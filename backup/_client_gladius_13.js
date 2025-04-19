/**
 * A minimal reactive framework providing signals, effects, and DOM rendering.
 * @module gladius.js
 */

let activeEffects = [];
let componentContextStack = [];

function h(type, props, ...children) {
  return {
    type,
    props: props || {},
    children: children.flat().filter(child => child != null && child !== false),
  };
}

function effect(fn) {
  let isDisposed = false;
  let cleanup = null;
  const dependencies = new Set();

  const effect = () => {
    if (isDisposed) return;

    dependencies.forEach(dep => dep.delete(effect));
    dependencies.clear();

    if (cleanup) {
      cleanup();
      cleanup = null;
    }

    activeEffects.push(effect);
    const newCleanup = fn();
    activeEffects.pop();

    if (typeof newCleanup === 'function') {
      cleanup = newCleanup;
    }

    const currentComponent = componentContextStack[componentContextStack.length - 1];
    if (currentComponent) {
      currentComponent._effects.push(() => {
        dependencies.forEach(dep => dep.delete(effect));
        dependencies.clear();
        if (cleanup) cleanup();
      });
    }
  };

  effect.execute = () => {
    if (isDisposed) return;
    effect();
  };

  effect.dependencies = dependencies;
  effect.cleanup = cleanup;

  effect();

  return () => {
    if (isDisposed) return;
    isDisposed = true;
    dependencies.forEach(dep => dep.delete(effect));
    dependencies.clear();
    if (cleanup) cleanup();
  };
}

function signal(initialValue) {
  let value = initialValue;
  const subscribers = new Set();

  const get = () => {
    const currentEffect = activeEffects[activeEffects.length - 1];
    if (currentEffect) {
      subscribers.add(currentEffect);
      currentEffect.dependencies.add(subscribers);
    }
    return value;
  };

  const set = newValue => {
    if (value === newValue) return;
    value = newValue;
    subscribers.forEach(effect => effect.execute());
  };

  return [get, set];
}

function createElement(node) {
  if (typeof node === 'string' || typeof node === 'number') {
    return document.createTextNode(node.toString());
  }

  if (typeof node.type === 'function') {
    const instance = { _effects: [] };
    componentContextStack.push(instance);
    const childNode = node.type({ ...node.props, children: node.children });
    componentContextStack.pop();
    const element = createElement(childNode);
    element._effects = instance._effects;

    const update = () => {
      const newInstance = { _effects: [] };
      componentContextStack.push(newInstance);
      const newChildNode = node.type({ ...node.props, children: node.children });
      componentContextStack.pop();
      const newElement = createElement(newChildNode);
      morph(element, newElement);
      newElement._effects.forEach(e => element._effects.push(e));
      element._effects.push(...newInstance._effects);
    };

    const dispose = effect(update);
    element._effects.push(dispose);

    return element;
  } else {
    const element = document.createElement(node.type);

    if (node.props) {
      Object.entries(node.props).forEach(([key, value]) => {
        if (key === 'class') {
          element.className = value;
        } else if (key.startsWith('on') && typeof value === 'function') {
          const eventName = key.slice(2).toLowerCase();
          element.addEventListener(eventName, value);
        } else {
          element.setAttribute(key, value);
        }
      });
    }

    node.children.forEach(child => {
      const childElement = createElement(child);
      element.appendChild(childElement);
    });

    return element;
  }
}

function morph(oldElement, newElement) {
  if (oldElement.nodeType !== newElement.nodeType || oldElement.nodeName !== newElement.nodeName) {
    if (oldElement.parentNode) {
      oldElement.parentNode.replaceChild(newElement, oldElement);
      if (oldElement._effects) {
        oldElement._effects.forEach(dispose => dispose());
      }
    }
    return;
  }

  if (oldElement.nodeType === Node.TEXT_NODE) {
    if (oldElement.textContent !== newElement.textContent) {
      oldElement.textContent = newElement.textContent;
    }
    return;
  }

  const newProps = newElement.props || {};
  const oldProps = {};

  Array.from(oldElement.attributes).forEach(attr => {
    oldProps[attr.name] = attr.value;
  });

  Object.entries(newProps).forEach(([key, value]) => {
    if (key === 'class') {
      if (oldElement.className !== value) {
        oldElement.className = value;
      }
    } else if (key.startsWith('on') && typeof value === 'function') {
      const eventName = key.slice(2).toLowerCase();
      const oldValue = oldProps[key];
      if (oldValue) {
        oldElement.removeEventListener(eventName, oldValue);
      }
      oldElement.addEventListener(eventName, value);
    } else {
      if (oldElement.getAttribute(key) !== String(value)) {
        oldElement.setAttribute(key, value);
      }
    }
  });

  Array.from(oldElement.attributes).forEach(attr => {
    if (!(attr.name in newProps)) {
      oldElement.removeAttribute(attr.name);
    }
  });

  const oldChildren = Array.from(oldElement.childNodes);
  const newChildren = Array.from(newElement.childNodes);
  const maxLen = Math.max(oldChildren.length, newChildren.length);

  for (let i = 0; i < maxLen; i++) {
    const oldChild = oldChildren[i];
    const newChild = newChildren[i];

    if (!oldChild && newChild) {
      oldElement.appendChild(newChild);
    } else if (oldChild && !newChild) {
      oldElement.removeChild(oldChild);
      if (oldChild._effects) {
        oldChild._effects.forEach(dispose => dispose());
      }
    } else {
      morph(oldChild, newChild);
    }
  }
}

function render(node, container) {
  const currentElement = container.firstChild;
  const newElement = createElement(node);

  if (currentElement) {
    morph(currentElement, newElement);
  } else {
    container.appendChild(newElement);
  }
}

// export { h, effect, signal, createElement, morph, render };
