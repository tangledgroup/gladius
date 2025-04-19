const observers = [];
const elementCleanupMap = new WeakMap();
let currentElement = null;

function h(type, props, ...children) {
  return { type, props, children };
}

function effect(fn) {
  let cleanup;
  let isDisposed = false;

  const execute = () => {
    if (isDisposed) return;

    if (cleanup) {
      cleanup();
      cleanup = null;
    }

    observers.push(execute);

    try {
      const result = fn();
      if (typeof result === 'function') {
        cleanup = result;

        if (currentElement) {
          if (!elementCleanupMap.has(currentElement)) {
            elementCleanupMap.set(currentElement, new Set());
          }
          elementCleanupMap.get(currentElement).add(cleanup);
        }
      }
    } finally {
      observers.pop();
    }
  };

  execute();

  const dispose = () => {
    if (isDisposed) return;
    isDisposed = true;
    if (cleanup) {
      cleanup();
    }
    if (currentElement && elementCleanupMap.has(currentElement)) {
      elementCleanupMap.get(currentElement).delete(cleanup);
    }
  };

  return dispose;
}

function signal(value) {
  const subscribers = new Set();

  const getValue = () => {
    const currentObserver = observers[observers.length - 1];
    if (currentObserver) {
      subscribers.add(currentObserver);
    }
    return value;
  };

  const setValue = (newValue) => {
    value = newValue;
    subscribers.forEach(sub => sub());
  };

  return [getValue, setValue];
}

function createElement(node) {
  if (typeof node === 'string' || typeof node === 'number' || typeof node === 'boolean') {
    return document.createTextNode(node.toString());
  }

  if (typeof node.type === 'function') {
    const prevElement = currentElement;
    const componentResult = node.type(node.props);
    const element = createElement(componentResult);
    currentElement = prevElement;
    return element;
  }

  const element = document.createElement(node.type);
  const prevElement = currentElement;
  currentElement = element;

  const props = node.props || {};
  for (const [key, value] of Object.entries(props)) {
    if (key.startsWith('on') && typeof value === 'function') {
      const eventName = key.slice(2).toLowerCase();
      element.addEventListener(eventName, value);
    } else if (key === 'class') {
      element.className = value;
    } else if (key === 'style' && typeof value === 'object') {
      Object.assign(element.style, value);
    } else if (key in element) {
      element[key] = value;
    } else {
      element.setAttribute(key, value);
    }
  }

  const flatten = (children) => children.reduce((acc, child) => (
    Array.isArray(child) ? acc.concat(flatten(child)) : (child != null && child !== false ? acc.concat(child) : acc)
  ), []);

  const children = flatten(node.children || []);
  for (const child of children) {
    const childElement = createElement(child);
    element.appendChild(childElement);
  }

  currentElement = prevElement;
  return element;
}

function morph(oldNode, newNode) {
  if (!oldNode || !oldNode.parentNode) return;

  if (typeof newNode === 'string' || typeof newNode === 'number' || typeof newNode === 'boolean') {
    if (oldNode.nodeType === Node.TEXT_NODE) {
      if (oldNode.textContent !== String(newNode)) {
        oldNode.textContent = newNode;
      }
    } else {
      const newElement = document.createTextNode(String(newNode));
      oldNode.parentNode.replaceChild(newElement, oldNode);
      const cleanups = elementCleanupMap.get(oldNode);
      if (cleanups) {
        cleanups.forEach(dispose => dispose());
        elementCleanupMap.delete(oldNode);
      }
    }
    return;
  }

  if (typeof newNode.type === 'function') {
    const componentResult = newNode.type(newNode.props);
    morph(oldNode, componentResult);
    return;
  }

  if (oldNode.nodeType !== Node.ELEMENT_NODE || oldNode.tagName.toLowerCase() !== newNode.type.toLowerCase()) {
    const newElement = createElement(newNode);
    oldNode.parentNode.replaceChild(newElement, oldNode);
    const cleanups = elementCleanupMap.get(oldNode);
    if (cleanups) {
      cleanups.forEach(dispose => dispose());
      elementCleanupMap.delete(oldNode);
    }
    return;
  }

  const newProps = newNode.props || {};
  const oldProps = Array.from(oldNode.attributes).reduce((acc, attr) => {
    acc[attr.name] = attr.value;
    return acc;
  }, {});

  for (const name of Object.keys(oldProps)) {
    if (!(name in newProps)) {
      oldNode.removeAttribute(name);
    }
  }

  for (const [name, value] of Object.entries(newProps)) {
    if (name.startsWith('on') && typeof value === 'function') {
      const eventName = name.slice(2).toLowerCase();
      const oldValue = oldProps[name];
      if (oldValue) {
        oldNode.removeEventListener(eventName, oldValue);
      }
      oldNode.addEventListener(eventName, value);
    } else if (name === 'class') {
      oldNode.className = value;
    } else if (name === 'style' && typeof value === 'object') {
      Object.assign(oldNode.style, value);
    } else if (name in oldNode) {
      oldNode[name] = value;
    } else {
      oldNode.setAttribute(name, value);
    }
  }

  const flatten = (children) => children.reduce((acc, child) => (
    Array.isArray(child) ? acc.concat(flatten(child)) : (child != null && child !== false ? acc.concat(child) : acc)
  ), []);

  const oldChildren = Array.from(oldNode.childNodes);
  const newChildren = flatten(newNode.children || []);

  for (let i = 0; i < Math.max(oldChildren.length, newChildren.length); i++) {
    const oldChild = oldChildren[i];
    const newChild = newChildren[i];
    if (oldChild && newChild) {
      morph(oldChild, newChild);
    } else if (newChild) {
      const newElement = createElement(newChild);
      oldNode.appendChild(newElement);
    } else if (oldChild) {
      oldNode.removeChild(oldChild);
      const cleanups = elementCleanupMap.get(oldChild);
      if (cleanups) {
        cleanups.forEach(dispose => dispose());
        elementCleanupMap.delete(oldChild);
      }
    }
  }
}

function render(node, container) {
  const curElement = container.firstChild;
  const newElement = createElement(node);

  if (curElement) {
    morph(curElement, node);
  } else {
    container.appendChild(newElement);
  }
}
