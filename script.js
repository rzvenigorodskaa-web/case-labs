document.addEventListener("DOMContentLoaded", () => {
    const studentForm = document.getElementById("studentForm");
    const studentTableBody = document.querySelector("#studentTable tbody");
    const movementLog = document.getElementById("movementLog");

    // Загружаем данные из localStorage
    let students = JSON.parse(localStorage.getItem("students")) || {};
    let log = JSON.parse(localStorage.getItem("movementLogDPO")) || [];

    // Сохранение
    function saveStudents() {
        localStorage.setItem("students", JSON.stringify(students));
    }

    function saveLog() {
        localStorage.setItem("movementLogDPO", JSON.stringify(log));
    }

    // Отображение таблицы слушателей
    function renderStudents() {
        studentTableBody.innerHTML = "";
        for (const name in students) {
            const program = students[name];
            const row = studentTableBody.insertRow();
            row.insertCell().textContent = name;
            row.insertCell().textContent = program;

            const deleteCell = row.insertCell();
            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Отчислить";
            deleteButton.classList.add("delete-btn");
            deleteButton.onclick = () => deleteStudent(name);
            deleteCell.appendChild(deleteButton);
        }
        saveStudents();
    }

    // Отображение истории (ИСПРАВЛЕННАЯ СТРОКА)
    function renderLog() {
        movementLog.innerHTML = "";
        log.slice().reverse().forEach((entry) => {
            const listItem = document.createElement("li");
            // Теперь при отчислении пишется "ОТЧИСЛЕН с программы"
            listItem.textContent = `${new Date(entry.timestamp).toLocaleString()} | ${entry.name} — ${entry.type === "add" ? "ЗАЧИСЛЕН на программу" : "ОТЧИСЛЕН с программы"}: ${entry.program}`;
            movementLog.appendChild(listItem);
        });
    }

    // Добавление записи в историю
    function addToLog(name, program, type) {
        log.push({ name, program, type, timestamp: new Date().toISOString() });
        if (log.length > 100) log.shift();
        saveLog();
        renderLog();
    }

    // Отчисление слушателя
    function deleteStudent(name) {
        if (confirm(`Вы уверены, что хотите отчислить "${name}"?`)) {
            const program = students[name];
            addToLog(name, program, "remove");
            delete students[name];
            renderStudents();
        }
    }

    // Обработка формы (зачисление/отчисление)
    studentForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const nameInput = document.getElementById("studentName");
        const programSelect = document.getElementById("program");
        const movementType = document.getElementById("movementType").value;

        const name = nameInput.value.trim();
        const program = programSelect.value;

        if (!name) {
            alert("Пожалуйста, введите ФИО слушателя.");
            return;
        }

        if (movementType === "add") {
            // Зачисление
            students[name] = program;
            addToLog(name, program, "add");
            alert(`Слушатель ${name} зачислен на программу "${program}"`);
        } else if (movementType === "remove") {
            // Отчисление
            if (!students[name]) {
                alert(`Слушатель "${name}" не найден в списке.`);
                return;
            }
            const oldProgram = students[name];
            addToLog(name, oldProgram, "remove");
            delete students[name];
            alert(`Слушатель ${name} отчислен`);
        }

        renderStudents();
        studentForm.reset();
        document.getElementById("studentName").focus();
    });

    renderStudents();
    renderLog();
});