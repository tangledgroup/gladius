declare const window: any;
const { signal, effect, render } = window;

const App = (props) => {
  return (
    <button class="primary">Click me</button>
  );
};

effect(() => {
  render(<App />, document.body);
  feather.replace();
});
