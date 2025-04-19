/**
 * A minimal reactive framework providing signals, effects, and efficient DOM rendering via hyperscript nodes and morphing.
 * @module gladius.js
 */
const observers = [];

function h(type, props, ...children) {
  // `esbuild` transpiles JSX/TSX into `h` calls to create "hyperscript" nodes for declarative UI construction.
  return { type, props, children };
}

function effect(fn) {
  // Effect is called to encapsulate signals into closure,
  // so when they are updated, then `fn` callback is fired.
  // `fn` can return `cleanup` function or null.
  // If `fn` returns function it is called when DOM element is removed from DOM on `morph` call.
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

function signal(initValue) {
  // Creates signal on initial value `value.
  // On setting new value, it notifies all subscribers.
  // returns tuple of getter and setter functions.
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

function createElement(node) {
  // from hyperscript node creates DOM element
}

function morph(oldElement, newElement) {
  // recursively goes over whole DOM tree of oldElement and newElement
  // compares them and deactivates signals and effects which are not in use any more
  // it takes care that signals and effects are not re-registered causing unnecessary render calls
}

function render(node, container) {
  // updates curElement based on diff between curElement and newElement
  const curElement = container.firstChild;
  const newElement = createElement(node);

  if (curElement) {
    morph(curElement, newElement);
  } else {
    container.appendChild(newElement);
  }
}
