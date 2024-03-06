const selectOrg = document.getElementById('id_organization')
const selectDep = document.getElementById('id_department')
const selectEx = document.getElementById('id_еxecutor')

selectDep.innerHTML = '';
selectEx.innerHTML = '';

var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

selectOrg.addEventListener('change', function(event){
    if (selectDep.childNodes.length){
        selectDep.innerHTML = '';
    }
    const val = event.target.value;
    $.ajax({
        url: '',
        type: "GET",
        dataType: "json",
        success: (data) => {
          console.log(data);
        },
        error: (error) => {
          console.log(error);
        }
      });
})
