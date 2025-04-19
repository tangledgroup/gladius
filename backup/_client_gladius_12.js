/**
 * A minimal reactive framework providing signals, effects, and DOM rendering.
 * @module gladius.js
 */

// Track active effect during execution
let activeEffect = null;
const effectsMap = new WeakMap();

function h(type, props, ...children) {
  // Flatten nested arrays of children
  const flatChildren = children.flat(Infinity).filter(c => c != null);
  return { type, props: props || {}, children: flatChildren };
}

function effect(fn) {
  // Create effect wrapper that will be called when dependencies change
  const effectFn = () => {
    // Clean up previous subscriptions before re-running
    cleanupDependencies(effectFn);

    // Clean up previous execution's cleanup if exists
    if (effectFn.cleanup && typeof effectFn.cleanup === 'function') {
      effectFn.cleanup();
      effectFn.cleanup = null;
    }

    // Set this effect as active to track dependencies
    const prevEffect = activeEffect;
    activeEffect = effectFn;

    // Execute effect and store cleanup if returned
    try {
      effectFn.cleanup = fn();
    } finally {
      // Restore previous active effect
      activeEffect = prevEffect;
    }
  };

  // Store subscribed signals
  effectFn.dependencies = new Set();

  // Run effect immediately
  effectFn();

  return effectFn;
}

// Helper to clean up an effect's dependencies
function cleanupDependencies(effectFn) {
  // Unsubscribe from all current dependencies
  for (const dep of effectFn.dependencies) {
    dep.delete(effectFn);
  }
  effectFn.dependencies.clear();
}

function signal(initialValue) {
  let value = initialValue;
  // Store effects that depend on this signal
  const subscribers = new Set();

  const getValue = () => {
    // If there's an active effect, subscribe it to this signal
    if (activeEffect) {
      subscribers.add(activeEffect);
      activeEffect.dependencies.add(subscribers);
    }
    return value;
  };

  const setValue = (newValue) => {
    if (value === newValue) return;
    value = newValue;

    // Create a snapshot of current subscribers to avoid modification during iteration
    const currentSubscribers = new Set(subscribers);
    for (const effectFn of currentSubscribers) {
      effectFn();
    }
  };

  return [getValue, setValue];
}

function createElement(node) {
  if (typeof node === 'string' || typeof node === 'number') {
    return document.createTextNode(node.toString());
  }

  if (node === null || node === undefined) {
    return document.createTextNode('');
  }

  // Handle functional components
  if (typeof node.type === 'function') {
    const result = node.type(node.props);
    return createElement(result);
  }

  // Create DOM element
  const element = document.createElement(node.type);

  // Add properties
  for (const [key, value] of Object.entries(node.props || {})) {
    if (key.startsWith('on') && typeof value === 'function') {
      // Event handlers
      const eventName = key.toLowerCase().substring(2);
      element.addEventListener(eventName, value);
    } else if (key === 'class' || key === 'className') {
      element.className = value;
    } else if (key === 'style' && typeof value === 'object') {
      Object.assign(element.style, value);
    } else if (key !== 'children' && key !== 'key') {
      // Set attribute
      element.setAttribute(key, value);
    }
  }

  // Add children
  for (const child of node.children || []) {
    element.appendChild(createElement(child));
  }

  return element;
}

function cleanupEffects(element) {
  // Clean up effects for this element
  if (element._effects) {
    for (const effectFn of element._effects) {
      cleanupDependencies(effectFn);

      if (effectFn.cleanup && typeof effectFn.cleanup === 'function') {
        effectFn.cleanup();
        effectFn.cleanup = null;
      }
    }
    element._effects = null;
  }

  // Recursively cleanup child elements
  for (const child of element.childNodes) {
    cleanupEffects(child);
  }
}

// Keep track of component instances
const componentCache = new WeakMap();

function morph(oldElement, newElement) {
  // If elements are different types
  if (oldElement.nodeType !== newElement.nodeType ||
      (oldElement.nodeType === Node.ELEMENT_NODE && oldElement.tagName.toLowerCase() !== newElement.tagName.toLowerCase())) {
    // Replace entire element and clean up effects
    cleanupEffects(oldElement);
    oldElement.parentNode.replaceChild(newElement, oldElement);
    return;
  }

  // Text node case
  if (oldElement.nodeType === Node.TEXT_NODE) {
    if (oldElement.textContent !== newElement.textContent) {
      oldElement.textContent = newElement.textContent;
    }
    return;
  }

  // Update attributes for element nodes
  if (oldElement.nodeType === Node.ELEMENT_NODE) {
    // Remove old attributes not in new element
    for (const attr of [...oldElement.attributes]) {
      if (!newElement.hasAttribute(attr.name)) {
        oldElement.removeAttribute(attr.name);
      }
    }

    // Add/update new attributes
    for (const attr of [...newElement.attributes]) {
      if (oldElement.getAttribute(attr.name) !== attr.value) {
        oldElement.setAttribute(attr.name, attr.value);
      }
    }

    // Update event handlers
    const newProps = newElement._props || {};
    const oldProps = oldElement._props || {};

    // Remove old event handlers
    for (const key in oldProps) {
      if (key.startsWith('on') && typeof oldProps[key] === 'function') {
        const eventName = key.substring(2).toLowerCase();
        if (!newProps[key]) {
          oldElement.removeEventListener(eventName, oldProps[key]);
        }
      }
    }

    // Add new event handlers
    for (const key in newProps) {
      if (key.startsWith('on') && typeof newProps[key] === 'function') {
        const eventName = key.substring(2).toLowerCase();
        if (oldProps[key] !== newProps[key]) {
          if (oldProps[key]) {
            oldElement.removeEventListener(eventName, oldProps[key]);
          }
          oldElement.addEventListener(eventName, newProps[key]);
        }
      }
    }

    // Store new props for future reference
    oldElement._props = Object.assign({}, newProps);

    // Update children
    const oldChildren = Array.from(oldElement.childNodes);
    const newChildren = Array.from(newElement.childNodes);

    const maxLength = Math.max(oldChildren.length, newChildren.length);

    for (let i = 0; i < maxLength; i++) {
      // Add new child
      if (i >= oldChildren.length) {
        oldElement.appendChild(newChildren[i].cloneNode(true));
      }
      // Remove extra old child
      else if (i >= newChildren.length) {
        cleanupEffects(oldChildren[i]);
        oldElement.removeChild(oldChildren[i]);
      }
      // Update existing child
      else {
        morph(oldChildren[i], newChildren[i]);
      }
    }
  }
}

function render(node, container) {
  const curElement = container.firstChild;
  const newElement = createElement(node);

  if (curElement) {
    morph(curElement, newElement);
  } else {
    container.appendChild(newElement);
  }
}
