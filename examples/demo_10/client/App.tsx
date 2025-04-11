import feather from 'feather-icons';

declare const window: any;
const { signal, effect, render } = window;

const [newTodoItem, setNewTodoItem] = signal('');
const [todoItems, setTodoItems] = signal([]);

const Todo = (props) => {
  return (
    <div class="flex flex-col w-full h-screen justify-center items-center">
      <div>
        <TodoHeader />
        <TodoList />
      </div>
    </div>
  );
};

const TodoHeader = (props) => {
  return (
    <div class="flex">
      <input type="text"
        class="input"
        placeholder="Title..."
        value={newTodoItem()}
        onchange={(e) => {
          // console.log('!', e.target.value);
          setNewTodoItem(e.target.value);
        }} />

      <button class="btn btn-primary"
        onclick={(e) => {
          console.log(e);
          setTodoItems([...todoItems(), newTodoItem()]);
          setNewTodoItem('');
        }}>
        <i data-feather="plus"></i>
      </button>
    </div>
  );
};

const TodoList = (props) => {
  return (
    <ul class="w-full list bg-base-100 rounded-box shadow-md">
      <TodoItem />
      <TodoItem />
      <TodoItem />
      <TodoItem />
    </ul>
  );
};

const TodoItem = (props) => {
  return (
    <li class="flex list-row items-center justify-between">
      <div class="flex-1">Dio Lupa</div>

      <button class="btn btn-square btn-ghost">
        <i data-feather="trash"></i>
      </button>
    </li>
  );
};

const App = (props) => {
  return (
    <Todo />
  );
};

effect(() => {
  console.log(newTodoItem(), todoItems());
});

effect(() => {
  render(<App />, document.body);
  feather.replace();
});
