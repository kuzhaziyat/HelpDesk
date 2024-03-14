const selectOrg = document.getElementById('id_organization');
const selectDep = document.getElementById('id_department');
$(document).ready(function () {
    selectOrg.addEventListener('change', function (event) {
        const orgId = event.target.value;
        
        $.ajax({
            url: '/task/get_departments/' + orgId + '/', // Используйте обратные кавычки (`) для вставки значения переменной
            type: "GET",
            dataType: "json",
            success: (data) => {
                // Очищаем текущие варианты отделов
                $('#id_department').empty();
                // Добавляем новые варианты отделов на основе полученных данных
                $.each(data, function (index, department) {
                    $('#id_department').append('<option value="' + department.id + '">' + department.name + '</option>');
                });
            },
            error: (error) => {
                console.log(error);
            }
        });
    });
});