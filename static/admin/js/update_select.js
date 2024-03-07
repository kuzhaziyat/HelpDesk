const selectOrg = document.getElementById('id_organization');
const selectDep = document.getElementById('id_department');

selectOrg.addEventListener('change', function(event){
    const orgId = event.target.value;
    $.ajax({
        url: "/task/get_departments/"+orgId+"/", // Предполагается, что у вас есть URL, который возвращает список отделов для данной организации
        type: "GET",
        dataType: "json",
        success: (data) => {
            // Очищаем текущие варианты отделов
            selectDep.innerHTML = '';
            // Добавляем новые варианты отделов на основе полученных данных
            data.forEach((department) => {
                const option = document.createElement('option');
                option.text = department.name; // Предполагается, что у вас есть свойство 'name' для каждого отдела
                option.value = department.id; // Предполагается, что у вас есть свойство 'id' для каждого отдела
                selectDep.appendChild(option);
            });
        },
        error: (error) => {
            console.log(error);
        }
    });
});