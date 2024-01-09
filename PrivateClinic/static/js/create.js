let listD = [];
function add() {
    const soLuong = document.getElementById('soLuong');
    const cachDung = document.getElementById('cachDung');
    const tableBody = document.getElementById('table');
    const thuocSelect = document.getElementById('thuoc');
    const tenThuoc = thuocSelect.options[thuocSelect.selectedIndex].text;
    const maThuoc = thuocSelect.value


    if (thuocSelect.value!=='' && soLuong.value !== '' && cachDung.value !== '') {
        listD.push({
            "tenThuoc": tenThuoc,
            "maThuoc": maThuoc,
            "soLuong": soLuong.value,
            "cachDung": cachDung.value
        });

        // Clear input values
        soLuong.value = '';
        cachDung.value = '';

        // Update the table
        updateTable();
    }
}
function updateTable() {
    const tableBody = document.getElementById('table');
    tableBody.innerHTML = '';
    for (let i = 0; i < listD.length; i++) {
        const row = document.createElement('tr');
        row.innerHTML = `

                            <td>${i + 1}</td>
                            <td style="width: 500px;">
                                <input name="maThuoc" hidden value="${listD[i].maThuoc}" />
                                <div style="width:100%;">${listD[i].tenThuoc}<div/>
                            </td>
                            <td>
                                <input class="border-0" style="outline: none; width:100%;" name="soLuong" value="${listD[i].soLuong}"/>
                            </td>
                            <td>
                                <input class="border-0" style="outline: none; width:100%;" name="cachDung" value="${listD[i].cachDung}"/>
                            </td>
                                <td><div class="m-auto"><input type="button" class="btn btn-danger" onclick="deleteRow(this)"value="Xóa"/></div>

        `;
        tableBody.appendChild(row);
    }
}
function deleteRow(index) {
    if (confirm("Bạn có chắc muốn xóa!") == true)
        listD.splice(index, 1);
            updateTable();
}


let listApp = [];

function addAppointment() {
    var selectedRow = event.target.closest('tr');
    var maBN = selectedRow.querySelector('#maBN').innerText;
    var id_ds= selectedRow.querySelector('#id').innerText;
    var hoTen = selectedRow.querySelector('#hoTen').innerText;
    var gioiTinh = selectedRow.querySelector('#gioiTinh').innerText;
    var ngaySinh = selectedRow.querySelector('#ngaySinh').innerText;
    var diaChi = selectedRow.querySelector('#diaChi').innerText;
    var ngayHen = selectedRow.querySelector('#ngayHen').innerText;

    listApp.push({
        "maDS": id_ds,
        "maBN": maBN,
        "hoTen": hoTen,
        "gioiTinh": gioiTinh,
        "ngaySinh": ngaySinh,
        "diaChi": diaChi,
        "ngayHen": ngayHen
    });

    updateTableAppoint();
    selectedRow.remove();
}
function deleteRowAppoint(index) {
    var selectedRow = event.target.closest('tr');
    var hoTen = selectedRow.querySelector('td:nth-child(2)').innerText;
    var maBN = selectedRow.querySelector('td:nth-child(2) input[name=maBenhNhan]').value;
    var maDS = selectedRow.querySelector('td:nth-child(2) input[name=maDS]').value;
    var ngayHen = selectedRow.querySelector('td:nth-child(2) input[name=ngayHen]').value;
    var gioiTinh = selectedRow.querySelector('td:nth-child(3) ').innerText;
    var ngaySinh = selectedRow.querySelector('td:nth-child(4) ').innerText;
    var diaChi = selectedRow.querySelector('td:nth-child(5) ').innerText;
    var oldTableBody = document.getElementById('data-table');
   // Tạo một dòng mới cho bảng cũ
    var newRow = oldTableBody.insertRow(oldTableBody.rows.length);
    newRow.innerHTML = `
        <td id="id" >${maDS}</td>
        <td id="maBN" name="maBN">${maBN}</td>
        <td id="hoTen">${hoTen}</td>
        <td id="gioiTinh">${gioiTinh}</td>
        <td id="ngaySinh">${ngaySinh}</td>
        <td id="diaChi">${diaChi}</td>
        <td id="ngayHen">${ngayHen}</td>
        <td>
            <div class="m-auto"><input type="button" class="btn btn-primary" onclick="addAppointment()" value="Tạo"/></div>
        </td>
    `;
    // Xóa dòng từ bảng đã tạo
     listApp.splice(index, 1);
     updateTableAppoint();
}

function updateTableAppoint() {
    var tableBody = document.getElementById('table');
    tableBody.innerHTML = '';

    for (var i = 0; i < listApp.length; i++) {
        var row = document.createElement('tr');
        row.innerHTML = `
            <td>${i + 1}</td>
            <td>
                <input name="maDS" hidden value="${listApp[i].maDS}"/>
                <input name="maBenhNhan" hidden value="${listApp[i].maBN}"/>
                <input name="ngayHen" hidden value="${listApp[i].ngayHen}"/>
                <div name="hoTen" style="width:100%;">${listApp[i].hoTen}</div>
            </td>
            <td>
             <div name="gioiTinh" style="width:100%;">${listApp[i].gioiTinh}</div>
            </td>
            <td>
             <div name="ngaySinh" style="width:100%;">${listApp[i].ngaySinh}</div>
            </td>
            <td>
             <div name="diaChi" style="width:100%;">${listApp[i].diaChi}</div>
            </td>
            <td>
                <div class="m-auto"><input type="button" class="btn btn-danger" onclick="deleteRowAppoint(this)" value="X"/></div>
            </td>
        `;
        tableBody.appendChild(row);
    }
}
function tinhTongTien() {
            var rows = document.querySelectorAll("#table tbody tr");
            var tongTien = 0;

            rows.forEach(function(row) {
                var soLuong = parseInt(row.cells[1].textContent);
                var gia = parseFloat(row.cells[2].textContent.replace(' VND', ''));
                var thanhTien = soLuong * gia;
                tongTien += thanhTien;
            });

            // Hiển thị tổng tiền
            document.getElementById("tongTien").textContent = "Tổng tiền: " + tongTien.toFixed(2) + " VND";
        }

        // Gọi hàm khi trang được tải
        document.addEventListener("DOMContentLoaded", function() {
            tinhTongTien();
        });