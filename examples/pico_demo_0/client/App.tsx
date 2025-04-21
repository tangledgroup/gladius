import { signal, effect, render } from 'gladius';

const [count, setCount] = signal(0);

const ClickedButton = (props: any) => {
  effect(() => {
    console.log(`Clicked ${count()} time(s)`);

    return () => {
      console.log('cleanup from ClickedButton when current ClickedButton instance is released and unused anymore');
    };
  });

  return (
    <div>
      <button class="primary" onclick={e => setCount(count() + 1)}>
        {count() == 0 ? 'Click me' : `Clicked ${count()} time(s)`}
      </button>
      <br />
    </div>
  );
};

const App = (props: any) => {
  effect(() => {
    return () => {
      console.log('cleanup from App called when current App instance is released and unused anymore');
    };
  });

  return (
    <div class="container">
      <h1>Hello there</h1>
      <ClickedButton />
      <ClickedButton />
      <ClickedButton />
      <ClickedButton />
      <ClickedButton />
    </div>
  );
};

effect(() => {
  render(<App />, document.body);

  return () => {
    console.log('cleanup from top-level when document.body instance is released and unused anymore');
  };
});
