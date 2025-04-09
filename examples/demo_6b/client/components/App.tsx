import PineconeRouter from 'pinecone-router/src';
import Alpine from 'alpinejs';
import h from 'vhtml';
import { Main } from './Main';

declare const window: any;
window.Alpine = Alpine;
window.h = h;

document.addEventListener('alpine:init', (event) => {
  console.log('alpine:init', event);

  const notify_messages = (message: any) => {
    const items = Alpine.store('messages').items;
    items.push(message);
  };

  Alpine.store('messages', {
    'items': [],
    'notify': notify_messages,
  });

  document.body.innerHTML = App();
});

const send = window.send = (event: any) => {
  if (!(event.type == 'click' || (event.type == 'keydown' && event.key == 'Enter'))) {
    return;
  }

  if (event && event.preventDefault) {
    event.preventDefault();
  }

  const notify = Alpine.store('messages').notify;
  const message_input = document.querySelector('input#message') as HTMLInputElement;
  notify(message_input.value);
  message_input.value = '';
  message_input.focus();

  // console.log(window.f0(10, 20));
};

export const App = (props?: any) => {
  return <Main />;
};

Alpine.plugin(PineconeRouter);
Alpine.start();
