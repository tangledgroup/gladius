declare const window: any;
const { signal, effect, render } = window;

const [clicked, setClicked] = signal(0);

export const App = () => {
  const buttonClick = (e: any) => {
    setClicked(clicked() + 1);
  };

  return (
    <div>
      <h1>Gladius</h1>
      <button class="btn btn-primary" onclick={buttonClick}>
        {clicked() == 0 ? 'Click me' : `Clicked ${clicked()} time(s)`}
      </button>

      <br/>

      <button class="btn btn-secondary" onclick={() => setClicked(clicked() + 1)}>
        +
      </button>

      <button class="btn btn-secondary" onclick={() => setClicked(clicked() - 1)}>
        -
      </button>
    </div>
  );
};

effect(() => {
  render(App(), document.body);
});
