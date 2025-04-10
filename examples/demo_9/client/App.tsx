declare const window: any;

let nClicked: number = 0;

const buttonClick = (e: any) => {
  console.log(e);

  if (!e) return;

  nClicked += 1;
  e.target.innerHTML = `Clicked ${nClicked} time(s)`;
}

export const App = () => (
  <div>
    <h1>Gladius</h1>
    <button class="btn btn-primary" onclick={buttonClick}>Click me</button>
  </div>
);

window.render(App(), document.body);
