null = None

def h(type, props, *children):
    return {'type': type, 'props': props, 'children': children}

def Todo(props):
  return  h("div", { 'class': "flex flex-col w-full h-screen justify-center items-center" },
      h("div", null,
          h(TodoHeader, null),
          h(TodoList, null)));

def TodoHeader(props):
  return  h("div", { 'class': "flex" },  h(
    "input",
    {
      'type': "text",
      'class': "input",
      'placeholder': "Title..."
    }
  ),  h(
    "button",
    {
      'class': "btn btn-primary"
    },
     h("i", { "data-feather": "plus" })
  ));

def TodoList(props):
  return  h("ul", { 'class': "w-full list bg-base-100 rounded-box shadow-md" },
      h(TodoItem, null),
      h(TodoItem, null),
      h(TodoItem, null),
      h(TodoItem, null));

def TodoItem(props):
  return  h("li", { 'class': "flex list-row items-center justify-between" },
      h("div", { 'class': "flex-1" }, "Dio Lupa"),
      h("button", { 'class': "btn btn-square btn-ghost" },
          h("i", { "data-feather": "trash" })));

def App(props):
  return  h(Todo, null);

app = App({})
print(app)
