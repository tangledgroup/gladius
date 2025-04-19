const observers = [];

function h(type, props, ...children) {
  return { type, props, children };
}

function effect(fn) {
  const execute = () => {
    let cleanup = undefined;
    observers.push(execute);

    try {
      cleanup = fn();
    } finally {
      observers.pop();
    }

    return cleanup;
  };

  const cleanup = execute();

  if (typeof cleanup === 'function') {
    cleanup();
  }
}

function signal(value) {
  const subscribers = new Set();

  const getValue = () => {
    const current = observers[observers.length - 1];

    if (current) {
      subscribers.add(current);
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

function renderNode(vnode) {
  const createElement = (node) => {
    if (typeof node === 'string' || typeof node === 'number') {
      return document.createTextNode(node.toString());
    }

    if (typeof node.type === 'function') {
      // Handle component functions
      const componentName = node.type.name;
      const componentVnode = node.type(node.props);
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
  return element;
}

function render(node, root) {
  const curEl = root.children[0];
  const el = renderNode(node);

  root.innerHTML = '';
  root.appendChild(el);
}
