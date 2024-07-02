import { useState, useEffect } from 'react';
import './App.css';

function Header({ onChangeMode, children }) {
    return (
        <h1 className="header" onClick={onChangeMode}>
            {children}
        </h1>
    );
}

function TodoList({ todos, onToggle, onSelect, onDelete }) {
    return (
        <div className="todo-list">
            {todos.map((todo) => (
                <div className="todo-item" key={todo.id} onClick={() => onSelect(todo.id)}>
                    <input
                        type="checkbox"
                        checked={todo.checked}
                        onChange={(e) => {
                            e.stopPropagation();
                            onToggle(todo.id);
                        }} // stopPropagation to avoid triggering onSelect
                    />
                    <span>{todo.title}</span>
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onDelete(todo.id);
                        }}
                    >
                        삭제
                    </button>
                </div>
            ))}
        </div>
    );
}

function Create({ onCreate }) {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    const handleClick = () => {
        onCreate(title, content);
        setTitle('');
        setContent('');
    };

    return (
        <div className="create-form">
            <p>
                <input type="text" placeholder="할 일" value={title} onChange={(e) => setTitle(e.target.value)} />
            </p>
            <p>
                <textarea placeholder="상세 내용" value={content} onChange={(e) => setContent(e.target.value)} />
            </p>
            <p>
                <button type="button" onClick={handleClick}>
                    생성
                </button>
            </p>
        </div>
    );
}

function Article({ title, content }) {
    return (
        <article>
            <h2>{title}</h2>
            <p>{content}</p>
        </article>
    );
}

function App() {
    const [mode, setMode] = useState('HOME');
    const [id, setId] = useState(-1);
    const [todos, setTodos] = useState(() => {
        const storedTodos = localStorage.getItem('todos');
        return storedTodos ? JSON.parse(storedTodos) : [];
    });

    useEffect(() => {
        localStorage.setItem('todos', JSON.stringify(todos));
    }, [todos]);

    const handleToggle = (id) => {
        setTodos(todos.map((todo) => (todo.id === id ? { ...todo, checked: !todo.checked } : todo)));
    };

    const handleCreate = (title, content) => {
        setTodos([...todos, { id: todos.length, title, content, checked: false }]);
        setMode('HOME');
    };

    const handleSelect = (id) => {
        setMode('READ');
        setId(id);
    };

    const handleDelete = (id) => {
        setTodos(todos.filter((todo) => todo.id !== id));
    };

    let title, content;
    if (mode === 'HOME') {
        title = '환영해요!';
        content = '할 일을 선택하거나 새로 추가하세요.';
    } else if (mode === 'READ') {
        const todo = todos.find((todo) => todo.id === id);
        title = todo ? todo.title : '';
        content = todo ? todo.content : '';
    }

    return (
        <div className="container">
            <Header onChangeMode={() => setMode('HOME')}>Hayoung's TODO LIST</Header>
            <TodoList todos={todos} onToggle={handleToggle} onSelect={handleSelect} onDelete={handleDelete} />
            <Article title={title} content={content} />
            {mode === 'CREATE' && <Create onCreate={handleCreate} />}
            {mode === 'HOME' && <button onClick={() => setMode('CREATE')}>글 생성</button>}
            {mode === 'READ' && <button onClick={() => setMode('HOME')}>홈으로 돌아가기</button>}
        </div>
    );
}

export default App;
