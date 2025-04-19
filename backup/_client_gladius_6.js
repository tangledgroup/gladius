/**
 * A minimal reactive framework providing signals, effects, and efficient DOM rendering via virtual nodes and morphing.
 * @module gladius.js
 */

const observers = [];

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
 * Registers a reactive effect that automatically tracks dependencies and re-runs when they change.
 * @param {Function} fn - The effect function to execute
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
}

/**
 * Creates a reactive signal with getter and setter functions.
 * @template T
 * @param {T} value - Initial value of the signal
 * @returns {[() => T, (value: T) => void]} Tuple of [getter, setter]
 */
function signal(value) {
  const subscribers = new Set();

  function addSubscriber(obj) {
    subscribers.add(obj);
  }

  function removeSubscriber(obj) {
    subscribers.delete(obj);
  }

  const getValue = () => {
    const current = observers[observers.length - 1];

    if (current) {
      addSubscriber(current);
    }

    return value;
  };

  const setValue = (newValue) => {
    value = newValue;

    for (const subscriber of subscribers) {
      subscriber();
    }
  };

  return [getValue, setValue];
}

/**
 * Creates a DOM node from a virtual node (vnode) or text.
 * @param {string|number|Object} node - The virtual node or text to create a DOM node from.
 * @returns {Node} The created DOM node.
 */
function createDomNode(node) {
  if (typeof node === 'string' || typeof node === 'number') {
    // Text node
    return document.createTextNode(node.toString());
  } else if (typeof node.type === 'function') {
    // Component: call the function to get the child vnode
    const childVnode = node.type(node.props);
    return createDomNode(childVnode);
  } else {
    // Element: create the DOM element
    const el = document.createElement(node.type);
    // Set attributes and event handlers
    for (const [key, value] of Object.entries(node.props || {})) {
      if (key.startsWith('on')) {
        const eventName = key.slice(2).toLowerCase();
        el.addEventListener(eventName, value);
      } else {
        el.setAttribute(key, value);
      }
    }
    // Append children
    for (const child of node.children) {
      const childDom = createDomNode(child);
      el.appendChild(childDom);
    }
    // Store props for future updates
    el.__props = node.props || {};
    return el;
  }
}

/**
 * Updates the attributes and event listeners of a DOM element based on new props.
 * @param {HTMLElement} domNode - The DOM element to update.
 * @param {Object} props - The new properties to apply.
 */
function updateAttributes(domNode, props) {
  const oldProps = domNode.__props || {};
  const newProps = props || {};

  // Remove old attributes and event listeners not in new props
  for (const key in oldProps) {
    if (!(key in newProps)) {
      if (key.startsWith('on')) {
        const eventName = key.slice(2).toLowerCase();
        domNode.removeEventListener(eventName, oldProps[key]);
      } else {
        domNode.removeAttribute(key);
      }
    }
  }

  // Set new attributes and event listeners
  for (const key in newProps) {
    if (key.startsWith('on')) {
      const eventName = key.slice(2).toLowerCase();
      if (oldProps[key] !== newProps[key]) {
        if (oldProps[key]) {
          domNode.removeEventListener(eventName, oldProps[key]);
        }
        domNode.addEventListener(eventName, newProps[key]);
      }
    } else {
      if (oldProps[key] !== newProps[key]) {
        domNode.setAttribute(key, newProps[key]);
      }
    }
  }

  // Update stored props
  domNode.__props = newProps;
}

/**
 * Updates the children of a DOM element to match the new children list.
 * @param {HTMLElement} domNode - The DOM element whose children need to be updated.
 * @param {Array} newChildren - The new list of children (vnodes or text).
 */
function updateChildren(domNode, newChildren) {
  const oldChildren = Array.from(domNode.childNodes);
  const maxLength = Math.max(oldChildren.length, newChildren.length);

  for (let i = 0; i < maxLength; i++) {
    if (i < newChildren.length) {
      const newChild = newChildren[i];
      if (i < oldChildren.length) {
        // Update existing child
        morph(oldChildren[i], newChild);
      } else {
        // Append new child
        const newDomChild = createDomNode(newChild);
        domNode.appendChild(newDomChild);
      }
    } else {
      // Remove extra child
      domNode.removeChild(oldChildren[i]);
    }
  }
}

/**
 * Efficiently updates an existing DOM node to match a new virtual node.
 * @param {Node} oldNode - Existing DOM node to update
 * @param {string|number|Object} newNode - New virtual node or text to match
 */
function morph(oldNode, newNode) {
  if (typeof newNode === 'string' || typeof newNode === 'number') {
    // Text node
    if (oldNode.nodeType === Node.TEXT_NODE) {
      if (oldNode.nodeValue !== newNode.toString()) {
        oldNode.nodeValue = newNode.toString();
      }
    } else {
      // Replace with text node
      const newTextNode = document.createTextNode(newNode.toString());
      oldNode.parentNode.replaceChild(newTextNode, oldNode);
    }
  } else {
    // newNode is a vnode object
    if (typeof newNode.type === 'function') {
      // Component: render the component to get its vnode
      const childVnode = newNode.type(newNode.props);
      morph(oldNode, childVnode);
    } else {
      // Element
      if (oldNode.nodeType === Node.ELEMENT_NODE && oldNode.tagName.toLowerCase() === newNode.type.toLowerCase()) {
        // Same element type: update in place
        updateAttributes(oldNode, newNode.props);
        updateChildren(oldNode, newNode.children);
      } else {
        // Different type: replace the node
        const newDomNode = createDomNode(newNode);
        oldNode.parentNode.replaceChild(newDomNode, oldNode);
      }
    }
  }
}

/**
 * Renders a virtual node into a DOM container using efficient morphing.
 * @param {Object} vnode - The root virtual node to render
 * @param {HTMLElement} container - DOM element to contain the rendered output
 */
function render(vnode, container) {
  if (!container.firstChild) {
    // Initial render: create and append the DOM structure
    const domNode = createDomNode(vnode);
    container.appendChild(domNode);
  } else {
    // Subsequent render: update existing DOM with morph
    morph(container.firstChild, vnode);
  }
}
