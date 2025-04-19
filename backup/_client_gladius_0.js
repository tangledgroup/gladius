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
/*
function signal(value) {
  // const subscribers = new Set();
  const weakSubscribers = new WeakSet();
  const subscribers = new Set();

  function addSubscriber(obj) {
    weakSubscribers.add(obj);
    subscribers.add(obj);
  }

  function removeSubscriber(obj) {
    weakSubscribers.delete(obj);
    subscribers.delete(obj);
  }

  const getValue = () => {
    const current = observers[observers.length - 1];
    console.debug(weakSubscribers);
    console.debug(subscribers);

    if (current) {
      // subscribers.add(current);
      addSubscriber(current);
    }

    return value;
  };

  const setValue = (newValue) => {
    const removedSubscribers = new Set();
    value = newValue;

    for (const subscriber of subscribers) {
      if (!weakSubscribers.has(subscriber)) {
        removedSubscribers.add(subscriber);
      }
    }

    for (const subscriber of removedSubscribers) {
      removeSubscriber(subscriber);
    }

    for (const subscriber of subscribers) {
      subscriber();
    }
  };

  return [getValue, setValue];
}
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
    console.debug(subscribers);

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
 * Renders a virtual node into a DOM container replacing old DOM nodes
 * @param {VNode} vnode - The root virtual node to render
 * @param {HTMLElement} container - DOM element to contain the rendered output
 */
function renderReplace(vnode, container) {
  // Clear container before rendering new content
  container.innerHTML = '';

  /**
   * Converts a virtual node to a real DOM element, handling components and elements.
   * @param {VNode} node - The virtual node to convert
   * @returns {Node} Real DOM node
   */
  const createElement = (node) => {
    if (typeof node === 'string' || typeof node === 'number') {
      return document.createTextNode(node.toString());
    }

    if (typeof node.type === 'function') {
      // Handle component functions
      const props = { ...node.props, children: node.children };
      const componentVnode = node.type(props);
      return createElement(componentVnode);
    }

    // Create regular DOM element
    const element = document.createElement(node.type);

    // Set attributes and event handlers
    if (node.props) {
      Object.entries(node.props).forEach(([key, value]) => {
        if (key.startsWith('on')) {
          // Handle events (e.g., onClick)
          element[key.toLowerCase()] = value;
        } else {
          element.setAttribute(key, value);
        }
      });
    }

    // Recursively render children
    node.children.forEach(child => {
      element.appendChild(createElement(child));
    });

    return element;
  };

  // Start rendering process
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
      const componentVnode = node.type(props);
      return createElement(componentVnode);
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

    element._props = node.props; // Store props for morphing
    node.children.forEach(child => element.appendChild(createElement(child)));
    return element;
}

/**
  * Efficiently updates an existing DOM node to match a new virtual node.
  * @param {Node} oldNode - Existing DOM node to update
  * @param {Node} newNode - New virtual node to match
  */
function morph(oldNode, newNode) {
    if (oldNode.nodeType !== newNode.nodeType ||
      (oldNode.nodeType === Node.ELEMENT_NODE && oldNode.tagName !== newNode.tagName)) {
      oldNode.replaceWith(newNode);
      return;
    }

    if (oldNode.nodeType === Node.TEXT_NODE) {
        if (oldNode.textContent !== newNode.textContent) {
          oldNode.textContent = newNode.textContent;
        }

        return;
    }

    // Update attributes
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

    // Update event handlers from props
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

    // Morph children
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
        oldNode.removeChild(oldChild);
      }
    }
}
