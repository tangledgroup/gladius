function h(type, props, ...children) {
  // creates hyperscript `node` instace with type, props and children
  return { type, props, children };
}

function signal(initialValue) {
  // return getter and setter for signal
}

function effect(callback) {
  // track signals changes
  // if callback returns function, call it when it is appropriate to cleanup what callback created
}

function createElement(node) {
  // create DOM element from hyperscript node
}

function morph(currentElement, newElement) {
  // currentElement and newElement are DOM elements
  // update currentElement based on difference between currentElement and newElement
}

function render(node, container) {
  const currentElement = container.children[0];
  const newElement = createElement(node);
  morph(currentElement, newElement);
}
