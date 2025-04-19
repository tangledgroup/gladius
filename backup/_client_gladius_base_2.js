/**
 * A minimal reactive framework providing signals, effects, and DOM rendering.
 * @module gladius.js
 */

 function h(type, props, ...children) {
  // `esbuild` transpiles JSX/TSX into `h` calls to create "hyperscript" nodes for declarative UI construction.
  return { type, props, children };
}

function effect(fn) {
  // Effect is called to encapsulate signals into closure,
  // so when they are updated, then `fn` callback is fired.
  // `fn` can return `cleanup` function or null.
  // If `fn` returns function it is called when DOM element is removed from DOM on `morph` call.
}

function signal(value) {
  // Creates signal on initial value `value.
  // On setting new value, it notifies all subscribers.

  const getValue = () => {
    // gets current value
    return value;
  }

  const setValue = (newValue) => {
    // sets new value.
    // notifies all alive effects listening.
    value = newValue;
  }

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
