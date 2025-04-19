/**
 * A minimal reactive framework providing signals, effects, and efficient DOM rendering via virtual nodes and morphing.
 * @module gladius.js
 */

const observers = [];

// Tracks effects during component rendering
let currentComponentEffects = null;

/**
 * Creates a virtual DOM node (vnode) for declarative UI construction.
 * @param {string|Function} type - HTML tag name or component function
 * @param {Object|null} props - Element attributes and event handlers
 * @param {...(VNode|string|number)} children - Child elements/nodes
 * @returns {VNode} Virtual DOM node object
 */
function h(type, props, ...children) {
  return { type, props, children };
}

/**
 * Registers a reactive effect that tracks dependencies and re-runs when they change.
 * @param {Function} fn - The effect function to execute
 * @returns {Function} Cleanup function to dispose of the effect
 */
function effect(fn) {
  const execute = () => {
    observers.push(execute);
    try {
      fn();
    } finally {
      observers.pop();
    }
  };

  execute();

  const cleanup = () => {
    for (const [signal, subscribers] of signalSubscribers) {
      subscribers.delete(execute);
    }
  };

  // If rendering a component, associate this effect with the component's node
  if (currentComponentEffects) {
    currentComponentEffects.push(cleanup);
  }

  return cleanup;
}

/**
 * WeakMap to associate signals with their subscriber Sets
 * @type {WeakMap<Function, Set<Function>>}
 */
const signalSubscribers = new WeakMap();

/**
 * Creates a reactive signal with getter and setter functions.
 * @template T
 * @param {T} value - Initial value of the signal
 * @returns {[() => T, (value: T) => void]} Tuple of [getter, setter]
 */
function signal(value) {
  const subscribers = new Set();

  const getValue = () => {
    const current = observers[observers.length - 1];
    if (current) {
      subscribers.add(current);
    }
    return value;
  };

  signalSubscribers.set(getValue, subscribers);

  const setValue = (newValue) => {
    if (value !== newValue) {
      value = newValue;
      const toRun = new Set(subscribers);
      for (const subscriber of toRun) {
        subscriber();
      }
    }
  };

  return [getValue, setValue];
}

/**
 * Renders a virtual node into a DOM container replacing old DOM nodes
 * @param {VNode} vnode - The root virtual node to render
 * @param {HTMLElement} container - DOM element to contain the rendered output
 */
function renderReplace(vnode, container) {
  const oldNode = container.firstChild;
  if (oldNode) {
    cleanupNode(oldNode);
  }
  container.innerHTML = '';
  const element = createElement(vnode);
  container.appendChild(element);
}

/**
 * Renders a virtual node into a DOM container using efficient morphing.
 * @param {VNode} vnode - The root virtual node to render
 * @param {HTMLElement} container - DOM element to contain the rendered output
 */
function render(vnode, container) {
  const newNode = createElement(vnode);
  const oldNode = container.firstChild;

  if (oldNode) {
    morph(oldNode, newNode);
  } else {
    container.appendChild(newNode);
  }
}

/**
 * Converts a virtual node to a real DOM element, handling components and elements.
 * @param {VNode} node - The virtual node to convert
 * @returns {Node} Real DOM node
 */
function createElement(node) {
  if (typeof node === 'string' || typeof node === 'number') {
    return document.createTextNode(node.toString());
  }

  if (typeof node.type === 'function') {
    const props = { ...node.props, children: node.children };
    const componentEffects = [];
    const prevEffects = currentComponentEffects;
    currentComponentEffects = componentEffects;
    try {
      const componentVnode = node.type(props);
      const element = createElement(componentVnode);
      element._effects = componentEffects;
      return element;
    } finally {
      currentComponentEffects = prevEffects;
    }
  }

  const element = document.createElement(node.type);

  if (node.props) {
    Object.entries(node.props).forEach(([key, value]) => {
      if (key.startsWith('on')) {
        element[key.toLowerCase()] = value;
      } else {
        element.setAttribute(key, value);
      }
    });
  }

  element._effects = [];
  element._props = node.props;

  node.children.forEach(child => {
    const childElement = createElement(child);
    element.appendChild(childElement);
  });

  return element;
}

/**
 * Cleans up all effects associated with a DOM node and its descendants.
 * @param {Node} node - The DOM node to clean up
 */
function cleanupNode(node) {
  if (node._effects) {
    node._effects.forEach(cleanup => cleanup());
    node._effects = [];
  }
  Array.from(node.childNodes).forEach(cleanupNode);
}

/**
 * Efficiently updates an existing DOM node to match a new virtual node.
 * @param {Node} oldNode - Existing DOM node to update
 * @param {Node} newNode - New virtual node to match
 */
function morph(oldNode, newNode) {
  if (oldNode.nodeType !== newNode.nodeType ||
      (oldNode.nodeType === Node.ELEMENT_NODE && oldNode.tagName !== newNode.tagName)) {
    cleanupNode(oldNode);
    oldNode.replaceWith(newNode);
    return;
  }

  if (oldNode.nodeType === Node.TEXT_NODE) {
    if (oldNode.textContent !== newNode.textContent) {
      oldNode.textContent = newNode.textContent;
    }
    return;
  }

  const oldAttrs = oldNode.attributes;
  const newAttrs = newNode.attributes;

  for (let i = oldAttrs.length - 1; i >= 0; i--) {
    const { name } = oldAttrs[i];
    if (!newAttrs[name]) {
      oldNode.removeAttribute(name);
    }
  }

  for (const { name, value } of newAttrs) {
    if (oldNode.getAttribute(name) !== value) {
      oldNode.setAttribute(name, value);
    }
  }

  const oldProps = oldNode._props || {};
  const newProps = newNode._props || {};

  Object.keys(oldProps).forEach(key => {
    if (key.startsWith('on') && !newProps[key]) {
      oldNode[key.toLowerCase()] = null;
    }
  });

  Object.keys(newProps).forEach(key => {
    if (key.startsWith('on')) {
      const newValue = newProps[key];
      const oldValue = oldProps[key];
      if (newValue !== oldValue) {
        oldNode[key.toLowerCase()] = newValue;
      }
    }
  });

  newNode._effects = oldNode._effects || [];
  oldNode._props = newProps;

  const oldChildren = Array.from(oldNode.childNodes);
  const newChildren = Array.from(newNode.childNodes);
  const maxLength = Math.max(oldChildren.length, newChildren.length);

  for (let i = 0; i < maxLength; i++) {
    const oldChild = oldChildren[i];
    const newChild = newChildren[i];

    if (oldChild && newChild) {
      morph(oldChild, newChild);
    } else if (newChild) {
      oldNode.appendChild(newChild);
    } else if (oldChild) {
      cleanupNode(oldChild);
      oldNode.removeChild(oldChild);
    }
  }
}
