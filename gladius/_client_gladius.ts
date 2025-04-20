import { h } from 'sinuous';
import { observable, subscribe, cleanup } from 'sinuous/observable';

declare const window: any;
window.h = h;
window.Fragment = null; // FIXME: implement

function signal(value: any): any {
  const o = observable(value);

  const getValue = () => {
    return o();
  }

  const setValue = (newValue: any): any => {
    o(newValue);
  }

  return [getValue, setValue];
}

function effect(fn: any): any {
  return subscribe(() => {
    const r = fn();

    if (r instanceof Function) {
      cleanup(r);
    }
  });
}

function morph(currentElement: any, newElement: any): any {
  // Replace if node types differ
  if (currentElement.nodeType !== newElement.nodeType) {
    currentElement.replaceWith(newElement);
    return;
  }

  // Handle text nodes
  if (currentElement.nodeType === Node.TEXT_NODE) {
    if (currentElement.textContent !== newElement.textContent) {
      currentElement.textContent = newElement.textContent;
    }
    return;
  }

  // Handle elements with different tags
  if (currentElement.tagName !== newElement.tagName) {
    currentElement.replaceWith(newElement);
    return;
  }

  // Update attributes
  Array.from(currentElement.attributes).forEach(attr => {
    if (!newElement.hasAttribute(attr.name)) {
      currentElement.removeAttribute(attr.name);
    }
  });
  Array.from(newElement.attributes).forEach(attr => {
    const currentValue = currentElement.getAttribute(attr.name);
    if (currentValue !== attr.value) {
      currentElement.setAttribute(attr.name, attr.value);
    }
  });

  // Morph children
  const currentChildren = Array.from(currentElement.childNodes);
  const newChildren = Array.from(newElement.childNodes);
  const maxLength = Math.max(currentChildren.length, newChildren.length);

  for (let i = 0; i < maxLength; i++) {
    const currentChild = currentChildren[i];
    const newChild = newChildren[i];

    if (currentChild && newChild) {
      morph(currentChild, newChild);
    } else if (newChild) {
      currentElement.appendChild(newChild.cloneNode(true));
    } else if (currentChild) {
      currentElement.removeChild(currentChild);
    }
  }
}

function render(newElement: any, container: any): any {
  if (container.firstChild) {
    morph(container.firstChild, newElement);
  } else {
    container.appendChild(newElement);
  }
}

export {
  h,
  signal,
  effect,
  morph,
  render,
};
