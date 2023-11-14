
$(document).ready( () => {
    $("#filter").on(); // TODO: Update
    $("#search").on("input", search);

    $("#modify-popup").on("show.bs.modal", modify);

    $("#save").on("click", submit);
    $("#remove").on("click", submit);
    $("[name='purchase']").on("click", purchase);
});

function search(){
    let key = $("#search").val().toLowerCase()

    $(".item.row").each((i, element) => {
        let row = $(element)
        if (row.attr("name").toLowerCase().includes(key)){
            row.css("display", "flex");
        } else {
            row.css("display", "none");
        }
    });
}

function filter(){
    // TODO: Add filter functionality
}

function modify(event){
    $("#modify-form")[0].reset()
    
    let id = Number($(event.relatedTarget).data("id"));

    if (id) {
        let item = shoppinglist[id];
        $("#id").val(id);
        $("#name").val(item.ingredient.name);
        $("#quantity").val(item.quantity);
        $("#unit").val(item.unit);
    }
}

function submit(){
    let form = $("#modify-form");
    let button = $(this);

    if (button.attr("id") == "save") {
        let id = Number($("#id").val());
        if (shoppinglist[id]){
            form.attr("action", "/shoppinglist/modify")
        } else {
            form.attr("action", "/shoppinglist/add")
        }
    } else {
        form.attr("action", "/shoppinglist/remove")
    }
    form.submit();
}

function purchase(){ // TODO: Add method of getting expiration date from the user.
    let form = $("#modify-form");
    let id = Number($(this).closest(".item.row").attr("id"));
    let item = shoppinglist[id];

    $("#id").val(id);
    $("#name").val(item.ingredient.name);
    $("#quantity").val(item.quantity);
    $("#unit").val(item.unit);

    form.attr("action", "/shoppinglist/purchase")
    form.submit();
}