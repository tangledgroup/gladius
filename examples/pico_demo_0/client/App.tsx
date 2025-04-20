import { signal, effect, render } from 'gladius';

const [clicked, setClicked] = signal(0);

const ClickedButton = (props: any) => {
  effect(() => {
    console.log(`Clicked ${clicked()} time(s)`);

    return () => {
      console.log('cleanup from ClickedButton when current ClickedButton instance is released and unused anymore');
    };
  });

  return (
    <div>
      <button class="primary" onclick={e => setClicked(clicked() + 1)}>
        {clicked() == 0 ? "Click me" : `Clicked ${clicked()} time(s)`}
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
