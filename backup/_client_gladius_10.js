let activeEffect = null;
let currentEffectContext = null;

class Effect {
  constructor(callback) {
    this.callback = callback;
    this.dependencies = new Set();
    this.cleanup = null;
  }

  execute() {
    this.dependencies.forEach(dep => dep.delete(this));
    this.dependencies.clear();

    const prevActive = activeEffect;
    activeEffect = this;
    try {
      const cleanup = this.callback();
      if (typeof cleanup === "function") {
        if (this.cleanup) this.cleanup();
        this.cleanup = cleanup;
      }
    } finally {
      activeEffect = prevActive;
    }
  }

  dispose() {
    this.dependencies.forEach(dep => dep.delete(this));
    this.dependencies.clear();
    if (this.cleanup) {
      this.cleanup();
      this.cleanup = null;
    }
  }
}

function h(type, props, ...children) {
  return { type, props: props || {}, children: children.flat() };
}

function signal(initialValue) {
  let value = initialValue;
  const subscribers = new Set();

  function getter() {
    if (activeEffect) {
      subscribers.add(activeEffect);
      activeEffect.dependencies.add(subscribers);
    }
    return value;
  }

  function setter(newValue) {
    if (Object.is(value, newValue)) return;
    value = newValue;
    subscribers.forEach(sub => sub.execute());
  }

  return [getter, setter];
}

function effect(callback) {
  const eff = new Effect(callback);
  eff.execute();

  if (currentEffectContext) {
    currentEffectContext.push(eff);
  }

  return () => eff.dispose();
}

function createElement(node) {
  if (typeof node === "string" || typeof node === "number") {
    return document.createTextNode(node.toString());
  }

  if (typeof node.type === "function") {
    const prevEffectContext = currentEffectContext;
    currentEffectContext = [];
    const childNode = node.type({ ...node.props, children: node.children });
    const element = createElement(childNode);
    if (currentEffectContext.length > 0) {
      element.__effects = currentEffectContext;
    }
    currentEffectContext = prevEffectContext;
    return element;
  }

  const element = document.createElement(node.type);

  Object.entries(node.props).forEach(([key, value]) => {
    if (key.startsWith("on") && typeof value === "function") {
      const eventName = key.slice(2).toLowerCase();
      element.addEventListener(eventName, value);
      element.__handlers = element.__handlers || {};
      if (element.__handlers[eventName]) {
        element.removeEventListener(eventName, element.__handlers[eventName]);
      }
      element.__handlers[eventName] = value;
    } else if (value !== undefined && value !== null) {
      element.setAttribute(key, value);
    }
  });

  node.children.forEach(child => {
    element.appendChild(createElement(child));
  });

  return element;
}

function cleanupEffects(element) {
  if (element.__effects) {
    element.__effects.forEach(effect => effect.dispose());
    element.__effects = null;
  }
  Array.from(element.childNodes).forEach(cleanupEffects);
}

function morph(currentNode, newNode) {
  if (!currentNode || !newNode) return newNode;
  if (currentNode.nodeType !== newNode.nodeType || currentNode.nodeName !== newNode.nodeName) {
    cleanupEffects(currentNode);
    const parent = currentNode.parentNode;
    parent?.replaceChild(newNode, currentNode);
    return newNode;
  }

  if (currentNode.nodeType === Node.TEXT_NODE) {
    if (currentNode.textContent !== newNode.textContent) {
      currentNode.textContent = newNode.textContent;
    }
    return currentNode;
  }

  // Update attributes
  const currentAttrs = Array.from(currentNode.attributes);
  const newAttrs = Array.from(newNode.attributes);

  currentAttrs
    .filter(attr => !newNode.hasAttribute(attr.name))
    .forEach(attr => currentNode.removeAttribute(attr.name));

  newAttrs.forEach(attr => {
    if (currentNode.getAttribute(attr.name) !== attr.value) {
      currentNode.setAttribute(attr.name, attr.value);
    }
  });

  // Update event handlers
  const currentHandlers = currentNode.__handlers || {};
  const newHandlers = newNode.__handlers || {};

  Object.keys(currentHandlers)
    .filter(eventName => !newHandlers[eventName])
    .forEach(eventName => {
      currentNode.removeEventListener(eventName, currentHandlers[eventName]);
      delete currentHandlers[eventName];
    });

  Object.entries(newHandlers).forEach(([eventName, handler]) => {
    if (currentHandlers[eventName] !== handler) {
      if (currentHandlers[eventName]) {
        currentNode.removeEventListener(eventName, currentHandlers[eventName]);
      }
      currentNode.addEventListener(eventName, handler);
      currentHandlers[eventName] = handler;
    }
  });

  // Update children
  const currentChildren = Array.from(currentNode.childNodes);
  const newChildren = Array.from(newNode.childNodes);
  const maxLength = Math.max(currentChildren.length, newChildren.length);

  for (let i = 0; i < maxLength; i++) {
    const currentChild = currentChildren[i];
    const newChild = newChildren[i];

    if (!newChild) {
      currentNode.removeChild(currentChild);
      cleanupEffects(currentChild);
    } else if (!currentChild) {
      currentNode.appendChild(newChild.cloneNode(true));
    } else {
      morph(currentChild, newChild);
    }
  }

  return currentNode;
}

function render(node, container) {
  const newEl = createElement(node);
  if (container.children[0]) {
    morph(container.children[0], newEl);
  } else {
    container.appendChild(newEl);
  }
}
