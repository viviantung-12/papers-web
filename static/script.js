// 取得所有論文並渲染表格
async function fetchPapers() {
    try {
        const res = await fetch("/api/papers");
        const papers = await res.json();
        renderTable(papers);
    } catch (err) {
        console.error("取得論文失敗:", err);
    }
}

// 渲染表格
function renderTable(papers) {
    const tbody = document.getElementById("paperBody");
    tbody.innerHTML = "";

    papers.forEach(p => {
        const tagsHtml = p.tags 
            ? p.tags.split(',').map(t => `<span class="tag">${t.trim()}</span>`).join(' ')
            : '';

        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${p.title}</td>
            <td>${p.author}</td>
            <td>${p.year || ""}</td>
            <td>${p.link ? `<a href="${p.link}" target="_blank">連結</a>` : ""}</td>
            <td>${p.abstract || ""}</td>
            <td>${tagsHtml}</td>
            <td><button class="delete-btn" onclick="deletePaper(${p.id})">刪除</button></td>
        `;
        tbody.appendChild(row);
    });
}

// 新增論文
async function addPaper() {
    const title = document.getElementById("title").value.trim();
    const author = document.getElementById("author").value.trim();
    const year = document.getElementById("year").value;
    const link = document.getElementById("link").value.trim();
    const abstract = document.getElementById("abstract").value.trim();
    const tags = document.getElementById("tags").value.trim();

    if (!title || !author) {
        alert("標題與作者為必填欄位！");
        return;
    }

    try {
        await fetch("/api/add", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({title, author, year, link, abstract, tags})
        });

        document.getElementById("title").value = "";
        document.getElementById("author").value = "";
        document.getElementById("year").value = "";
        document.getElementById("link").value = "";
        document.getElementById("abstract").value = "";
        document.getElementById("tags").value = "";

        fetchPapers();
    } catch (err) {
        console.error("新增論文失敗:", err);
        alert("新增論文失敗，請檢查伺服器是否正常運作。");
    }
}

// 刪除論文
async function deletePaper(id) {
    if (!confirm("確定要刪除這筆論文嗎？")) return;

    try {
        await fetch(`/api/delete/${id}`, { method: "DELETE" });
        fetchPapers();
    } catch (err) {
        console.error("刪除失敗:", err);
        alert("刪除失敗，請稍後再試。");
    }
}

// 初始載入
fetchPapers();
