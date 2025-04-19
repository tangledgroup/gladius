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

///

function createDomFromVnode(vnode) {
  // Handle function components
  if (typeof vnode.type === 'function') {
    const childVnode = vnode.type({ ...vnode.props, children: vnode.children });
    return createDomFromVnode(childVnode);
  }
  // Handle text nodes
  else if (typeof vnode === 'string' || typeof vnode === 'number') {
    return document.createTextNode(String(vnode));
  }
  // Handle element nodes
  else {
    const domNode = document.createElement(vnode.type);
    const props = vnode.props || {};
    // Set attributes and event handlers
    for (const key in props) {
      if (key.startsWith('on')) {
        domNode[key] = props[key];
      } else {
        domNode.setAttribute(key, props[key]);
      }
    }
    // Create and append children
    const children = vnode.children || [];
    for (const child of children) {
      const childDom = createDomFromVnode(child);
      domNode.appendChild(childDom);
    }
    return domNode;
  }
}

function morph(oldNode, newVnode) {
  // Handle function components
  if (typeof newVnode.type === 'function') {
    const childVnode = newVnode.type({ ...newVnode.props, children: newVnode.children });
    return morph(oldNode, childVnode);
  }
  // Handle text nodes
  else if (typeof newVnode === 'string' || typeof newVnode === 'number') {
    const newText = String(newVnode);
    if (oldNode.nodeType === Node.TEXT_NODE) {
      if (oldNode.textContent !== newText) {
        oldNode.textContent = newText;
      }
      return oldNode;
    } else {
      return document.createTextNode(newText);
    }
  }
  // Handle element nodes
  else if (oldNode.nodeType === Node.ELEMENT_NODE && oldNode.tagName.toLowerCase() === newVnode.type.toLowerCase()) {
    const props = newVnode.props || {};

    // Update attributes: set only changed attributes, handle event handlers
    for (const key in props) {
      if (key.startsWith('on')) {
        // Only update event handlers if different
        if (oldNode[key] !== props[key]) {
          oldNode[key] = props[key];
        }
      } else {
        const newValue = props[key];
        const oldValue = oldNode.getAttribute(key);
        if (oldValue !== newValue) {
          oldNode.setAttribute(key, newValue);
        }
      }
    }
    // Remove attributes not in new props
    const attrs = Array.from(oldNode.attributes);
    for (const attr of attrs) {
      const key = attr.name;
      if (!(key in props) && !key.startsWith('on')) {
        oldNode.removeAttribute(key);
      }
    }

    // Update children
    const oldChildren = Array.from(oldNode.childNodes);
    const newChildren = newVnode.children || [];
    const minLength = Math.min(oldChildren.length, newChildren.length);

    // Morph existing children
    for (let i = 0; i < minLength; i++) {
      const oldChild = oldChildren[i];
      const newChildVnode = newChildren[i];
      const updatedChild = morph(oldChild, newChildVnode);
      if (updatedChild !== oldChild) {
        oldNode.replaceChild(updatedChild, oldChild);
      }
    }
    // Append new children
    for (let i = oldChildren.length; i < newChildren.length; i++) {
      const newChildDom = createDomFromVnode(newChildren[i]);
      oldNode.appendChild(newChildDom);
    }
    // Remove extra children
    while (oldNode.childNodes.length > newChildren.length) {
      oldNode.removeChild(oldNode.lastChild);
    }

    return oldNode;
  }
  // Replace node if types differ
  else {
    return createDomFromVnode(newVnode);
  }
}

function render(vnode, container) {
  if (container.firstChild) {
    const newDomNode = morph(container.firstChild, vnode);
    if (newDomNode !== container.firstChild) {
      container.replaceChild(newDomNode, container.firstChild);
    }
  } else {
    const dom = createDomFromVnode(vnode);
    container.appendChild(dom);
  }
}
