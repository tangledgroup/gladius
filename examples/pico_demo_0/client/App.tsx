declare const window: any;
const { signal, effect, render } = window;

const [clicked, setClicked] = signal(0);

const ClickedButton = (props) => {
  effect(() => {
    console.log(`Clicked ${clicked()} time(s)`);
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

const App = (props) => {
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
});
