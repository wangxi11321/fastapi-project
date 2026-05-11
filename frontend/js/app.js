let currentModule = 'dashboard';

function showModule(moduleName) {
    document.querySelectorAll('.module').forEach(m => m.classList.remove('active'));
    document.getElementById(moduleName)?.classList.add('active');
    currentModule = moduleName;
    
    const loaders = { student: () => student.refresh(), course: () => course.refresh(), 
        score: () => score.refresh(), class: () => cls.refresh(), 
        department: () => dept.refresh(), employee: () => emp.refresh(),
        employment: () => employment.refresh() };
    
    if (loaders[moduleName]) loaders[moduleName]();
}

function showModal(content) {
    document.getElementById('modal-body').innerHTML = content;
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == document.getElementById('modal')) closeModal();
};

const student = {
    page: 1,
    async refresh() {
        try {
            const result = await StudentAPI.list(this.page);
            this.render(result.data || result);
            this.updatePagination(result);
        } catch (e) {
            this.showError(e.message);
        }
    },
    updatePagination(result) {
        const total = result.total || 0;
        const pageSize = 10;
        const totalPages = Math.ceil(total / pageSize);
        const pagination = document.getElementById('student-pagination');
        if (!pagination) return;
        
        let html = '';
        const startPage = Math.max(1, this.page - 2);
        const endPage = Math.min(totalPages, this.page + 2);
        
        if (this.page > 1) {
            html += `<button onclick="student.goPage(${this.page - 1})">上一页</button>`;
        }
        for (let i = startPage; i <= endPage; i++) {
            html += `<button onclick="student.goPage(${i})" class="${i === this.page ? 'active' : ''}">${i}</button>`;
        }
        if (this.page < totalPages) {
            html += `<button onclick="student.goPage(${this.page + 1})">下一页</button>`;
        }
        pagination.innerHTML = html;
    },
    goPage(page) {
        this.page = page;
        this.refresh();
    },
    render(data) {
        const tbody = document.querySelector('#student-table tbody');
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7">暂无数据</td></tr>';
            return;
        }
        tbody.innerHTML = data.map(s => `
            <tr>
                <td>${s.stu_id || s.stuId || '-'}</td>
                <td>${s.stu_name || s.stuName || '-'}</td>
                <td>${s.gender || '-'}</td>
                <td>${s.age || '-'}</td>
                <td>${s.class_id || s.classId || '-'}</td>
                <td>${s.major || '-'}</td>
                <td>
                    <button class="view" onclick="student.view(${s.stu_id || s.stuId})">查看</button>
                    <button class="edit" onclick="student.showEditDialog(${s.stu_id || s.stuId})">编辑</button>
                    <button class="delete" onclick="student.delete(${s.stu_id || s.stuId})">删除</button>
                </td>
            </tr>
        `).join('');
    },
    async search() {
        const stuId = document.getElementById('student-search-id').value;
        const stuName = document.getElementById('student-search-name').value;
        const classId = document.getElementById('student-search-class').value;
        if (!stuId) { alert('请输入学生ID'); return; }
        try {
            const result = await StudentAPI.search(stuId, stuName, classId);
            this.render(result.data ? [result.data] : [result]);
        } catch (e) { this.showError(e.message); }
    },
    async view(stuId) {
        try {
            const result = await StudentAPI.get(stuId);
            alert(JSON.stringify(result, null, 2));
        } catch (e) { alert('错误: ' + e.message); }
    },
    showAddDialog() {
        showModal(`
            <h2>新增学生</h2>
            <div class="form-row"><label>学生ID *</label><input type="number" id="s-stu_id" required></div>
            <div class="form-row"><label>学生姓名 *</label><input type="text" id="s-stu_name" required></div>
            <div class="form-row"><label>班级ID *</label><input type="number" id="s-class_id" required></div>
            <div class="form-row"><label>性别</label><input type="text" id="s-gender"></div>
            <div class="form-row"><label>年龄</label><input type="number" id="s-age"></div>
            <div class="form-row"><label>专业</label><input type="text" id="s-major"></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="student.create()">提交</button>
            </div>
        `);
    },
    async create() {
        const stuIdVal = document.getElementById('s-stu_id').value;
        const stuNameVal = document.getElementById('s-stu_name').value;
        const classIdVal = document.getElementById('s-class_id').value;
        if (!stuIdVal || !stuNameVal || !classIdVal) {
            alert('请填写必填字段');
            return;
        }
        const data = {
            stu_id: parseInt(stuIdVal),
            stu_name: stuNameVal,
            class_id: parseInt(classIdVal),
            gender: document.getElementById('s-gender').value || undefined,
            age: document.getElementById('s-age').value ? parseInt(document.getElementById('s-age').value) : undefined,
            major: document.getElementById('s-major').value || undefined
        };
        try {
            await StudentAPI.create(data);
            alert('创建成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showEditDialog(stuId) {
        showModal(`
            <h2>编辑学生</h2>
            <div class="form-row"><label>学生姓名</label><input type="text" id="e-stu_name"></div>
            <div class="form-row"><label>性别</label><input type="text" id="e-gender"></div>
            <div class="form-row"><label>年龄</label><input type="number" id="e-age"></div>
            <div class="form-row"><label>专业</label><input type="text" id="e-major"></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="student.update(${stuId})">提交</button>
            </div>
        `);
    },
    async update(stuId) {
        const data = {};
        const name = document.getElementById('e-stu_name').value;
        const gender = document.getElementById('e-gender').value;
        const age = document.getElementById('e-age').value;
        const major = document.getElementById('e-major').value;
        if (name) data.stu_name = name;
        if (gender) data.gender = gender;
        if (age) data.age = parseInt(age);
        if (major) data.major = major;
        try {
            await StudentAPI.update(stuId, data);
            alert('更新成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    async delete(stuId) {
        if (!confirm('确定要删除该学生吗？')) return;
        try {
            await StudentAPI.delete(stuId);
            alert('删除成功');
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showError(msg) {
        const tbody = document.querySelector('#student-table tbody');
        tbody.innerHTML = `<tr><td colspan="7" class="error">${msg}</td></tr>`;
    }
};

const course = {
    async refresh() {
        try {
            const result = await CourseAPI.list();
            this.render(result.data || []);
        } catch (e) { this.showError(e.message); }
    },
    render(data) {
        const tbody = document.querySelector('#course-table tbody');
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4">暂无数据</td></tr>';
            return;
        }
        tbody.innerHTML = data.map(c => `
            <tr>
                <td>${c.course_id || c.courseId || '-'}</td>
                <td>${c.course_name || c.courseName || '-'}</td>
                <td>${c.create_time || '-'}</td>
                <td>
                    <button class="edit" onclick="course.showEditDialog(${c.course_id || c.courseId})">编辑</button>
                    <button class="delete" onclick="course.delete(${c.course_id || c.courseId})">删除</button>
                </td>
            </tr>
        `).join('');
    },
    showAddDialog() {
        showModal(`
            <h2>新增课程</h2>
            <div class="form-row"><label>课程ID *</label><input type="number" id="c-course_id" required></div>
            <div class="form-row"><label>课程名称 *</label><input type="text" id="c-course_name" required></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="course.create()">提交</button>
            </div>
        `);
    },
    async create() {
        const courseId = document.getElementById('c-course_id').value;
        const courseName = document.getElementById('c-course_name').value;
        if (!courseId || !courseName) {
            alert('请填写必填字段');
            return;
        }
        try {
            await CourseAPI.create({ course_id: parseInt(courseId), course_name: courseName });
            alert('创建成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showEditDialog(courseId) {
        showModal(`
            <h2>编辑课程</h2>
            <div class="form-row"><label>课程名称</label><input type="text" id="e-course_name"></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="course.update(${courseId})">提交</button>
            </div>
        `);
    },
    async update(courseId) {
        const name = document.getElementById('e-course_name').value;
        if (!name) { alert('请填写课程名称'); return; }
        try {
            await CourseAPI.update(courseId, { course_name: name });
            alert('更新成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    async delete(courseId) {
        if (!confirm('确定要删除该课程吗？')) return;
        try {
            await CourseAPI.delete(courseId);
            alert('删除成功');
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showError(msg) {
        const tbody = document.querySelector('#course-table tbody');
        tbody.innerHTML = `<tr><td colspan="4" class="error">${msg}</td></tr>`;
    }
};

const score = {
    async refresh() {
        try {
            const result = await ScoreAPI.list();
            this.render(result.data || []);
        } catch (e) { this.showError(e.message); }
    },
    render(data) {
        const tbody = document.querySelector('#score-table tbody');
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5">暂无数据</td></tr>';
            return;
        }
        tbody.innerHTML = data.map(s => `
            <tr>
                <td>${s.stu_id || s.stuId || '-'}</td>
                <td>${s.exam_course_id || s.courseId || '-'}</td>
                <td>${s.test_num || s.testNum || '-'}</td>
                <td>${s.score || '-'}</td>
                <td>
                    <button class="delete" onclick="score.delete('${s.stu_id}', ${s.test_num || s.testNum}, ${s.exam_course_id || s.courseId})">删除</button>
                </td>
            </tr>
        `).join('');
    },
    showAddDialog() {
        showModal(`
            <h2>新增成绩</h2>
            <div class="form-row"><label>学生ID *</label><input type="number" id="sc-stu_id" required></div>
            <div class="form-row"><label>课程ID *</label><input type="number" id="sc-exam_course_id" required></div>
            <div class="form-row"><label>考试次数 *</label><input type="number" id="sc-test_num" required></div>
            <div class="form-row"><label>成绩 *</label><input type="number" id="sc-score" step="0.01" required></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="score.create()">提交</button>
            </div>
        `);
    },
    async create() {
        const stuId = document.getElementById('sc-stu_id').value;
        const courseId = document.getElementById('sc-exam_course_id').value;
        const testNum = document.getElementById('sc-test_num').value;
        const scoreVal = document.getElementById('sc-score').value;
        if (!stuId || !courseId || !testNum || !scoreVal) {
            alert('请填写必填字段');
            return;
        }
        try {
            await ScoreAPI.create({
                stu_id: parseInt(stuId),
                exam_course_id: parseInt(courseId),
                test_num: parseInt(testNum),
                score: parseFloat(scoreVal)
            });
            alert('创建成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    async delete(stuId, testNum, courseId) {
        if (!confirm('确定要删除该成绩吗？')) return;
        try {
            await ScoreAPI.delete(stuId, testNum, courseId);
            alert('删除成功');
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showError(msg) {
        const tbody = document.querySelector('#score-table tbody');
        tbody.innerHTML = `<tr><td colspan="5" class="error">${msg}</td></tr>`;
    }
};

const cls = {
    async refresh() {
        try {
            const result = await ClassAPI.list();
            this.render(result.data || []);
        } catch (e) { this.showError(e.message); }
    },
    render(data) {
        const tbody = document.querySelector('#class-table tbody');
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5">暂无数据</td></tr>';
            return;
        }
        tbody.innerHTML = data.map(c => `
            <tr>
                <td>${c['班级id'] || c.class_id || c.classId || '-'}</td>
                <td>${c['班级名称'] || c.class_name || c.className || '-'}</td>
                <td>${c['班主任编号'] || c.head_teacher_id || c.teacher_id || '-'}</td>
                <td>${c['班级状态'] || c.class_status || '正常'}</td>
                <td>
                    <button class="view" onclick="cls.viewStudents(${c['班级id'] || c.class_id || c.classId})">学生</button>
                    <button class="edit" onclick="cls.showEditDialog(${c['班级id'] || c.class_id || c.classId})">编辑</button>
                    <button class="delete" onclick="cls.delete(${c['班级id'] || c.class_id || c.classId})">删除</button>
                </td>
            </tr>
        `).join('');
    },
    async viewStudents(classId) {
        try {
            const result = await ClassAPI.students(classId);
            alert(JSON.stringify(result, null, 2));
        } catch (e) { alert('错误: ' + e.message); }
    },
    showAddDialog() {
        showModal(`
            <h2>新增班级</h2>
            <div class="form-row"><label>班级ID *</label><input type="number" id="cl-class_id" required></div>
            <div class="form-row"><label>班级名称 *</label><input type="text" id="cl-class_name" required></div>
            <div class="form-row"><label>班主任ID</label><input type="number" id="cl-teacher_id"></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="cls.create()">提交</button>
            </div>
        `);
    },
    async create() {
        const data = {
            class_id: parseInt(document.getElementById('cl-class_id').value),
            class_name: document.getElementById('cl-class_name').value,
            head_teacher_id: parseInt(document.getElementById('cl-teacher_id').value) || null
        };
        try {
            await ClassAPI.create(data);
            alert('创建成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showEditDialog(classId) {
        showModal(`
            <h2>编辑班级</h2>
            <div class="form-row"><label>班级名称</label><input type="text" id="e-class_name"></div>
            <div class="form-row"><label>班主任ID</label><input type="number" id="e-teacher_id"></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="cls.update(${classId})">提交</button>
            </div>
        `);
    },
    async update(classId) {
        const data = {};
        const name = document.getElementById('e-class_name').value;
        const teacher = document.getElementById('e-teacher_id').value;
        if (name) data.class_name = name;
        if (teacher) data.head_teacher_id = parseInt(teacher);
        try {
            await ClassAPI.update(classId, data);
            alert('更新成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    async delete(classId) {
        if (!confirm('确定要删除该班级吗？')) return;
        try {
            await ClassAPI.delete(classId);
            alert('删除成功');
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showError(msg) {
        const tbody = document.querySelector('#class-table tbody');
        tbody.innerHTML = `<tr><td colspan="5" class="error">${msg}</td></tr>`;
    }
};

const dept = {
    page: 1,
    async refresh() {
        try {
            const result = await DepartmentAPI.list(this.page);
            this.render(result.data || []);
        } catch (e) { this.showError(e.message); }
    },
    render(data) {
        const tbody = document.querySelector('#dept-table tbody');
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3">暂无数据</td></tr>';
            return;
        }
        tbody.innerHTML = data.map(d => `
            <tr>
                <td>${d.department_id || d.departmentId || '-'}</td>
                <td>${d.department_name || d.departmentName || '-'}</td>
                <td>
                    <button class="edit" onclick="dept.showEditDialog(${d.department_id || d.departmentId})">编辑</button>
                    <button class="delete" onclick="dept.delete(${d.department_id || d.departmentId})">删除</button>
                </td>
            </tr>
        `).join('');
    },
    showAddDialog() {
        showModal(`
            <h2>新增部门</h2>
            <div class="form-row"><label>部门ID *</label><input type="number" id="d-department_id" required></div>
            <div class="form-row"><label>部门名称 *</label><input type="text" id="d-department_name" required></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="dept.create()">提交</button>
            </div>
        `);
    },
    async create() {
        const deptId = document.getElementById('d-department_id').value;
        const deptName = document.getElementById('d-department_name').value;
        if (!deptId || !deptName) {
            alert('请填写必填字段');
            return;
        }
        try {
            await DepartmentAPI.create({ department_id: parseInt(deptId), department_name: deptName });
            alert('创建成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showEditDialog(deptId) {
        showModal(`
            <h2>编辑部门</h2>
            <div class="form-row"><label>部门名称</label><input type="text" id="e-department_name"></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="dept.update(${deptId})">提交</button>
            </div>
        `);
    },
    async update(deptId) {
        const name = document.getElementById('e-department_name').value;
        if (!name) { alert('请填写部门名称'); return; }
        try {
            await DepartmentAPI.update(deptId, { department_name: name });
            alert('更新成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    async delete(deptId) {
        if (!confirm('确定要删除该部门吗？')) return;
        try {
            await DepartmentAPI.delete(deptId);
            alert('删除成功');
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showError(msg) {
        const tbody = document.querySelector('#dept-table tbody');
        tbody.innerHTML = `<tr><td colspan="3" class="error">${msg}</td></tr>`;
    }
};

const emp = {
    async refresh() {
        try {
            const result = await EmployeeAPI.list();
            this.render(Array.isArray(result) ? result : (result.data || []));
        } catch (e) { this.showError(e.message); }
    },
    render(data) {
        const tbody = document.querySelector('#emp-table tbody');
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5">暂无数据</td></tr>';
            return;
        }
        tbody.innerHTML = data.map(e => `
            <tr>
                <td>${e.employee_id || e.employeeId || e.id || '-'}</td>
                <td>${e.employee_name || e.name || '-'}</td>
                <td>${e.position_name || e.position || '-'}</td>
                <td>${e.department_id || e.departmentId || '-'}</td>
                <td>
                    <button class="edit" onclick="emp.showEditDialog(${e.employee_id || e.employeeId || e.id})">编辑</button>
                    <button class="delete" onclick="emp.delete(${e.employee_id || e.employeeId || e.id})">删除</button>
                </td>
            </tr>
        `).join('');
    },
    async search() {
        const name = document.getElementById('employee-search-name').value;
        if (!name) { alert('请输入员工姓名'); return; }
        try {
            const result = await EmployeeAPI.search(name);
            this.render(result.data || [result]);
        } catch (e) { this.showError(e.message); }
    },
    showAddDialog() {
        showModal(`
            <h2>新增员工</h2>
            <div class="form-row"><label>员工ID *</label><input type="number" id="em-employee_id" required></div>
            <div class="form-row"><label>姓名 *</label><input type="text" id="em-emp_name" required></div>
            <div class="form-row"><label>职位</label><input type="text" id="em-position"></div>
            <div class="form-row"><label>部门ID</label><input type="number" id="em-department_id"></div>
            <div class="form-row"><label>薪资</label><input type="number" id="em-salary"></div>
            <div class="form-row"><label>入职时间</label><input type="date" id="em-hire_time"></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="emp.create()">提交</button>
            </div>
        `);
    },
    async create() {
        const empId = document.getElementById('em-employee_id').value;
        const empName = document.getElementById('em-emp_name').value;
        if (!empId || !empName) {
            alert('请填写必填字段');
            return;
        }
        const data = {
            employee_id: parseInt(empId),
            employee_name: empName,
            position_name: document.getElementById('em-position').value || '',
            department_id: document.getElementById('em-department_id').value || '1',
            salary: document.getElementById('em-salary').value ? parseInt(document.getElementById('em-salary').value) : 0,
            hire_time: document.getElementById('em-hire_time').value || '2025-01-01'
        };
        try {
            await EmployeeAPI.create(data);
            alert('创建成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showEditDialog(empId) {
        showModal(`
            <h2>编辑员工</h2>
            <div class="form-row"><label>姓名</label><input type="text" id="e-emp_name"></div>
            <div class="form-row"><label>职位</label><input type="text" id="e-position"></div>
            <div class="form-row"><label>部门ID</label><input type="number" id="e-department_id"></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="emp.update(${empId})">提交</button>
            </div>
        `);
    },
    async update(empId) {
        const data = {};
        const name = document.getElementById('e-emp_name').value;
        const position = document.getElementById('e-position').value;
        const deptId = document.getElementById('e-department_id').value;
        if (name) data.employee_name = name;
        if (position) data.position_name = position;
        if (deptId) data.department_id = parseInt(deptId);
        try {
            await EmployeeAPI.update(empId, data);
            alert('更新成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    async delete(empId) {
        if (!confirm('确定要删除该员工吗？')) return;
        try {
            await EmployeeAPI.delete(empId);
            alert('删除成功');
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showError(msg) {
        const tbody = document.querySelector('#emp-table tbody');
        tbody.innerHTML = `<tr><td colspan="5" class="error">${msg}</td></tr>`;
    }
};

const employment = {
    async refresh() {
        try {
            const result = await EmploymentAPI.list();
            this.render(Array.isArray(result) ? result : (result.data || []));
        } catch (e) { this.showError(e.message); }
    },
    render(data) {
        const tbody = document.querySelector('#employment-table tbody');
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6">暂无数据</td></tr>';
            return;
        }
        tbody.innerHTML = data.map(e => `
            <tr>
                <td>${e.stu_id || e.stuId || '-'}</td>
                <td>${e.class_id || e.classId || '-'}</td>
                <td>${e.employment_status || e.status || '-'}</td>
                <td>${e.employment_company_name || e.companyName || '-'}</td>
                <td>${e.salary || '-'}</td>
                <td>
                    <button class="edit" onclick="employment.showEditDialog(${e.stu_id || e.stuId})">编辑</button>
                    <button class="delete" onclick="employment.delete(${e.stu_id || e.stuId})">删除</button>
                </td>
            </tr>
        `).join('');
    },
    async search() {
        const stuId = document.getElementById('employment-search-stu').value;
        const classId = document.getElementById('employment-search-class').value;
        try {
            let result;
            if (stuId) {
                result = await EmploymentAPI.getByStudent(stuId);
            } else if (classId) {
                result = await EmploymentAPI.getByClass(classId);
            } else {
                alert('请输入学生ID或班级ID');
                return;
            }
            this.render(result.data || [result]);
        } catch (e) { this.showError(e.message); }
    },
    showAddDialog() {
        showModal(`
            <h2>新增就业信息</h2>
            <div class="form-row"><label>学生ID *</label><input type="number" id="em-stu_id" required></div>
            <div class="form-row"><label>班级ID</label><input type="number" id="em-class_id"></div>
            <div class="form-row"><label>就业状态</label><input type="text" id="em-status"></div>
            <div class="form-row"><label>公司名称</label><input type="text" id="em-company"></div>
            <div class="form-row"><label>薪资</label><input type="number" id="em-salary"></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="employment.create()">提交</button>
            </div>
        `);
    },
    async create() {
        const stuId = document.getElementById('em-stu_id').value;
        if (!stuId) {
            alert('请填写学生ID');
            return;
        }
        const data = {
            stu_id: parseInt(stuId),
            class_id: document.getElementById('em-class_id').value ? parseInt(document.getElementById('em-class_id').value) : undefined,
            employment_status: document.getElementById('em-status').value || undefined,
            employment_company_name: document.getElementById('em-company').value || undefined,
            salary: document.getElementById('em-salary').value ? parseFloat(document.getElementById('em-salary').value) : undefined
        };
        try {
            await EmploymentAPI.create(data);
            alert('创建成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showEditDialog(stuId) {
        showModal(`
            <h2>编辑就业信息</h2>
            <div class="form-row"><label>就业状态</label><input type="text" id="e-status"></div>
            <div class="form-row"><label>公司名称</label><input type="text" id="e-company"></div>
            <div class="form-row"><label>薪资</label><input type="number" id="e-salary"></div>
            <div class="form-actions">
                <button class="cancel" onclick="closeModal()">取消</button>
                <button class="submit" onclick="employment.update(${stuId})">提交</button>
            </div>
        `);
    },
    async update(stuId) {
        const data = {};
        const status = document.getElementById('e-status').value;
        const company = document.getElementById('e-company').value;
        const salary = document.getElementById('e-salary').value;
        if (status) data.employment_status = status;
        if (company) data.employment_company_name = company;
        if (salary) data.salary = parseFloat(salary);
        try {
            await EmploymentAPI.update(stuId, data);
            alert('更新成功');
            closeModal();
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    async delete(stuId) {
        if (!confirm('确定要删除该就业信息吗？')) return;
        try {
            await EmploymentAPI.delete(stuId);
            alert('删除成功');
            this.refresh();
        } catch (e) { alert('错误: ' + e.message); }
    },
    showError(msg) {
        const tbody = document.querySelector('#employment-table tbody');
        tbody.innerHTML = `<tr><td colspan="6" class="error">${msg}</td></tr>`;
    }
};

function loadStats() {
    Promise.all([
        StatsAPI.highScore(),
        StatsAPI.lowScore(),
        StatsAPI.avgScore(),
        StatsAPI.top5Salary()
    ]).then(results => {
        const statHigh = document.getElementById('stat-high');
        const statLow = document.getElementById('stat-low');
        const statAvg = document.getElementById('stat-avg');
        const statTop5 = document.getElementById('stat-top5');
        if (statHigh) statHigh.textContent = results[0].data?.length || 0;
        if (statLow) statLow.textContent = results[1].data?.length || 0;
        if (statAvg) statAvg.textContent = (results[2].data?.avg_score || 0).toFixed(1);
        if (statTop5) statTop5.textContent = results[3].data?.length || 0;
    }).catch(e => console.error('加载统计数据失败:', e));
}

document.addEventListener('DOMContentLoaded', loadStats);

const stats = {
    async highScore() {
        try {
            const result = await StatsAPI.highScore();
            this.showResult('高分学生(80分以上)', result);
        } catch (e) { this.showError(e.message); }
    },
    async lowScore() {
        try {
            const result = await StatsAPI.lowScore();
            this.showResult('低分不及格学生', result);
        } catch (e) { this.showError(e.message); }
    },
    async avgScore() {
        try {
            const result = await StatsAPI.avgScore();
            this.showResult('班级平均分排名', result);
        } catch (e) { this.showError(e.message); }
    },
    async courseCount() {
        try {
            const result = await StatsAPI.courseCount();
            this.showResult('课程数量统计', result);
        } catch (e) { this.showError(e.message); }
    },
    async courseStudents() {
        try {
            const result = await StatsAPI.courseStudents();
            this.showResult('每门课程学生统计', result);
        } catch (e) { this.showError(e.message); }
    },
    async deptCount() {
        try {
            const result = await StatsAPI.deptCount();
            this.showResult('部门数量统计', result);
        } catch (e) { this.showError(e.message); }
    },
    async deptEmployees() {
        try {
            const result = await StatsAPI.deptEmployees();
            this.showResult('部门员工统计', result);
        } catch (e) { this.showError(e.message); }
    },
    async over30() {
        try {
            const result = await StatsAPI.over30();
            this.showResult('30岁以上学生', result);
        } catch (e) { this.showError(e.message); }
    },
    async classStat() {
        try {
            const result = await StatsAPI.classStat();
            this.showResult('班级统计', result);
        } catch (e) { this.showError(e.message); }
    },
    async classCount() {
        try {
            const result = await StatsAPI.classCount();
            this.showResult('班级人数统计', result);
        } catch (e) { this.showError(e.message); }
    },
    async classAvgScore() {
        try {
            const result = await StatsAPI.classAvgScore();
            this.showResult('班级平均分', result);
        } catch (e) { this.showError(e.message); }
    },
    async empStats() {
        try {
            const result = await StatsAPI.empStats();
            this.showResult('员工统计', result);
        } catch (e) { this.showError(e.message); }
    },
    async empPosition() {
        try {
            const result = await StatsAPI.empPosition();
            this.showResult('按职位统计', result);
        } catch (e) { this.showError(e.message); }
    },
    async top5Salary() {
        try {
            const result = await StatsAPI.top5Salary();
            this.showResult('薪资Top5', result);
        } catch (e) { this.showError(e.message); }
    },
    async studentDuration() {
        try {
            const result = await StatsAPI.studentDuration();
            this.showResult('学生就业时长', result);
        } catch (e) { this.showError(e.message); }
    },
    async classAvgDuration() {
        try {
            const result = await StatsAPI.classAvgDuration();
            this.showResult('班级平均就业时长', result);
        } catch (e) { this.showError(e.message); }
    },
    showResult(title, data) {
        const container = document.getElementById('stats-result');
        let html = `<h4>${title}</h4>`;
        
        if (!data || typeof data !== 'object') {
            html += `<p>${data || '暂无数据'}</p>`;
        } else if (Array.isArray(data)) {
            html += this.arrayToTable(data);
        } else if (data.data && Array.isArray(data.data)) {
            html += this.arrayToTable(data.data);
        } else {
            html += this.objectToTable(data);
        }
        
        container.innerHTML = html;
    },
    
    arrayToTable(data) {
        if (!data || data.length === 0) {
            return '<p>暂无数据</p>';
        }
        
        const keys = Object.keys(data[0]);
        const chineseKeys = this.getChineseKeys(keys);
        
        let html = '<div class="stats-table-container"><table class="stats-table">';
        html += '<thead><tr>';
        keys.forEach(key => {
            html += `<th>${chineseKeys[key] || key}</th>`;
        });
        html += '</tr></thead><tbody>';
        
        data.forEach(row => {
            html += '<tr>';
            keys.forEach(key => {
                const value = row[key];
                const displayValue = this.formatValue(value);
                html += `<td>${displayValue}</td>`;
            });
            html += '</tr>';
        });
        
        html += '</tbody></table></div>';
        return html;
    },
    
    objectToTable(data) {
        let html = '<div class="stats-grid-display">';
        
        for (const [key, value] of Object.entries(data)) {
            const chineseKey = this.getChineseLabel(key);
            const displayValue = this.formatValue(value);
            html += `
                <div class="stats-item">
                    <span class="stats-label">${chineseKey || key}</span>
                    <span class="stats-value">${displayValue}</span>
                </div>
            `;
        }
        
        html += '</div>';
        return html;
    },
    
    getChineseKeys(keys) {
        const mapping = {
            'stu_id': '学生ID', 'stuId': '学生ID', 'student_id': '学生ID',
            'stu_name': '姓名', 'stuName': '姓名', 'student_name': '姓名',
            'class_id': '班级ID', 'classId': '班级ID', 'class_name': '班级名称',
            'score': '成绩', 'avg_score': '平均分', 'average_score': '平均分',
            'course_id': '课程ID', 'course_name': '课程名称',
            'department_id': '部门ID', 'department_name': '部门名称',
            'employee_id': '员工ID', 'employee_name': '员工姓名',
            'position_name': '职位', 'salary': '薪资', 'hire_time': '入职时间',
            'employment_status': '就业状态', 'employment_company_name': '公司名称',
            'company_city': '公司城市', 'company_type': '公司类型', 'job_position': '岗位',
            'gender': '性别', 'age': '年龄', 'major': '专业',
            'total_count': '总数', 'total': '总数', 'count': '数量',
            'male_count': '男生人数', 'female_count': '女生人数',
            'male_ratio': '男生比例', 'female_ratio': '女生比例',
            'employment_open_date': '就业开放日期', 'first_offer_date': '首份offer日期',
            'get_offer_num': '拿到offer数量', 'employment_date': '就业日期',
            'mployment_status': '就业状态', 'delete_flag': '删除标记',
            'creation_date': '创建日期', 'insert_date': '插入日期',
            'id': 'ID', 'name': '名称', 'value': '数值'
        };
        return mapping;
    },
    
    getChineseLabel(key) {
        const mapping = {
            'total_count': '总数', 'total': '总数', 'count': '数量',
            'avg_score': '平均分', 'average_score': '平均分',
            'message': '提示信息', 'data': '数据',
            'male_count': '男生人数', 'female_count': '女生人数',
            'male_ratio': '男生比例', 'female_ratio': '女生比例',
            'max_salary': '最高薪资', 'min_salary': '最低薪资',
            'avg_salary': '平均薪资', 'employee_count': '员工数量'
        };
        return mapping[key];
    },
    
    formatValue(value) {
        if (value === null || value === undefined) return '-';
        if (typeof value === 'number' && value % 1 !== 0) {
            return value.toFixed(2);
        }
        if (typeof value === 'boolean') {
            return value ? '是' : '否';
        }
        if (typeof value === 'string' && value.length > 50) {
            return value.substring(0, 50) + '...';
        }
        return value;
    },
    showError(msg) {
        const container = document.getElementById('stats-result');
        container.innerHTML = `<div class="error">${msg}</div>`;
    }
};