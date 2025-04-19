const observers = [];
const renderingStack = [];

function cleanupNode(node) {
  if (node._cleanups) {
    node._cleanups.forEach(cleanup => cleanup());
    node._cleanups = null;
  }
  Array.from(node.childNodes).forEach(cleanupNode);
}

function h(type, props, ...children) {
  return { type, props, children };
}

function effect(fn) {
  const execute = () => {
    observers.push(execute);
    try {
      fn();
    } finally {
      observers.pop();
    }
  };

  execute.cleanup = () => {
    if (execute._dependencies) {
      for (const getValue of execute._dependencies) {
        getValue.subscribers.delete(execute);
      }
      execute._dependencies.clear();
    }
  };

  const currentNode = renderingStack[renderingStack.length - 1];
  if (currentNode) {
    if (!currentNode._cleanups) currentNode._cleanups = [];
    currentNode._cleanups.push(execute.cleanup);
  }

  execute();
  return execute.cleanup;
}

function signal(value) {
  const subscribers = new Set();

  const getValue = () => {
    const current = observers[observers.length - 1];
    if (current) {
      subscribers.add(current);
      if (!current._dependencies) current._dependencies = new Set();
      current._dependencies.add(getValue);
    }
    return value;
  };

  getValue.subscribers = subscribers;

  const setValue = (newValue) => {
    if (value === newValue) return;
    value = newValue;
    // console.debug(subscribers);
    for (const subscriber of subscribers) subscriber();
  };

  return [getValue, setValue];
}

function renderReplace(vnode, container) {
  Array.from(container.childNodes).forEach(cleanupNode);
  container.innerHTML = '';
  const element = createElement(vnode);
  container.appendChild(element);
}

function render(vnode, container) {
  const newNode = createElement(vnode);
  const oldNode = container.firstChild;
  if (oldNode) morph(oldNode, newNode);
  else container.appendChild(newNode);
}

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
  renderingStack.push(element);

  if (node.props) {
    Object.entries(node.props).forEach(([key, value]) => {
      if (key.startsWith('on')) element[key.toLowerCase()] = value;
      else element.setAttribute(key, value);
    });
  }

  node.children.forEach(child => element.appendChild(createElement(child)));
  renderingStack.pop();
  return element;
}

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
    if (!newAttrs[name]) oldNode.removeAttribute(name);
  }

  for (const { name, value } of newAttrs) {
    if (oldNode.getAttribute(name) !== value) oldNode.setAttribute(name, value);
  }

  const oldProps = oldNode._props || {};
  const newProps = newNode._props || {};

  Object.keys(oldProps).forEach(key => {
    if (key.startsWith('on') && !newProps[key]) oldNode[key.toLowerCase()] = null;
  });

  Object.keys(newProps).forEach(key => {
    if (key.startsWith('on')) {
      const newValue = newProps[key];
      const oldValue = oldProps[key];
      if (newValue !== oldValue) oldNode[key.toLowerCase()] = newValue;
    }
  });

  const oldChildren = Array.from(oldNode.childNodes);
  const newChildren = Array.from(newNode.childNodes);
  const maxLength = Math.max(oldChildren.length, newChildren.length);

  for (let i = 0; i < maxLength; i++) {
    const oldChild = oldChildren[i];
    const newChild = newChildren[i];
    if (oldChild && newChild) morph(oldChild, newChild);
    else if (newChild) oldNode.appendChild(newChild);
    else if (oldChild) {
      cleanupNode(oldChild);
      oldNode.removeChild(oldChild);
    }
  }
}
