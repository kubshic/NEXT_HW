const todoForm = document.getElementById('todo-form'); // 투두입력 받는 form 태그
const contentInput = document.getElementById('content'); // 투두항목 입력 받는 input 태그
const todoList = document.getElementById('todo-list'); // 투두항목 나열되는 ul태그
const submitBtn = document.querySelector('.submitBtn'); // 투두항목 제출하는 버튼

let todos = JSON.parse(localStorage.getItem('todos')) || [];

function submitAddTodo(event) {
    event.preventDefault(); // 새로고침 방지

    const newTodo = contentInput.value.trim();
    if (newTodo === '') return; // Ignore empty input

    const todoObj = {
        id: Date.now(),
        text: newTodo,
    };

    todos.push(todoObj);
    saveTodos();
    paintTodo(todoObj);

    contentInput.value = ''; // Clear the input field
}

function paintTodo(todo) {
    const li = document.createElement('li');
    li.id = todo.id;

    const span = document.createElement('span');
    span.textContent = todo.text;

    const button = document.createElement('button');
    button.textContent = 'Delete';
    button.addEventListener('click', deleteTodo);

    li.appendChild(span);
    li.appendChild(button);
    todoList.appendChild(li);
}

function saveTodos() {
    localStorage.setItem('todos', JSON.stringify(todos));
}

function deleteTodo(event) {
    const li = event.target.parentElement;
    li.remove();
    todos = todos.filter((todo) => todo.id !== parseInt(li.id));
    saveTodos();
}

function loadTodos() {
    todos.forEach((todo) => paintTodo(todo));
}

document.addEventListener('DOMContentLoaded', loadTodos);
todoForm.addEventListener('submit', submitAddTodo);
