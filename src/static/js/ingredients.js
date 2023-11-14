
$(document).ready( () => {
    $("#filter").on(); // TODO: Update
    $("#search").on("input", search);

    $("#modify-popup").on("show.bs.modal", modify);

    $("#save").on("click", submit);
    $("#remove").on("click", submit);
});

function search(){
    let key = $("#search").val().toLowerCase()

    $(".item.row").each((i, element) => {
        if (row.children().eq(0).text().toLowerCase().includes(key)){
            $("#"+element.id).css("display", "flex");
        } else {
            $("#"+element.id).css("display", "none");
        }
    });
}

function filter(){
    // TODO: Add filter functionality
}

function modify(event){
    let id = Number($(event.relatedTarget).data("id"));

    if (id) {
        let item = inventory[id];
        $("#id").val(id);
        $("#name").val(item.ingredient.name);
        $("#quantity").val(item.quantity);
        $("#unit").val(item.unit);
        $("#expiration_date").val(item.expiration_date);
    }
}

function submit(){
    let form = $("#modify-form");
    let button = $(this);

    if (button.attr("id") == "save") {
        let id = Number($("#id"));
        if (inventory[id]){
            form.attr("action", "/ingredients/modify")  
        } else {
            form.attr("action", "/ingredients/add")  
        }
    } else {
        form.attr("action", "/ingredients/remove")  
    }

    form.submit();
    form.reset();
}

function remove(){
    let form = $("#modify-form");
    form.attr("action", "/ingredients/remove")
    form.submit();
    form.reset();

}

// let item_updates = {
//     ingredient: {
//         name: "", //TO-DO: fix
//         id: $("#m-ingredient").val()
//     },
//     quantity: $("#m-quantity").val(),
//     unit: $("#m-unit").val(),
//     expiration_date: $("#m-expiration_date").val()
// };
// console.log(item_updates)

// let item = inventory[id];
// let item_updates = {
//     ingredient: {
//         name: row.children().eq(0).text(),
//         id: id
//     },
//     quantity: Number(row.children().eq(1).text().split(" ")[0]),
//     unit: row.children().eq(1).text().split(" ")[1],
//     expiration_date: row.children().eq(2).text()
// };

// if (row.hasClass("bg-success")) {
//     inventory_updates[id] = item_updates;
// } else if (
//     item.ingredient.id != item_updates.ingredient.id ||
//     item.quantity != item_updates.quantity ||
//     item.unit != item_updates.unit ||
//     item.expiration_date != item_updates.expiration_date
// ) {
//     inventory_updates[id] = item_updates;
//     row.addClass("bg-warning");
// } else {
//     delete inventory_updates[id];
//     row.removeClass("bg-warning");
// }

// let table = $("#inventory");
// table.append(
//     `<div class="item row py-1 pe-1 border-top border-dark-subtle bg-opacity-25 bg-success" id="`+ item.ingredient.id + `" style="align-items: center;">
//         <div class="col-4">`+ item.ingredient.name + `</div>
//         <div class="col-4">`+ item.quantity + ` ` + item.unit + `</div>
//         <div class="col-3">`+ item.expiration_date + `</div>
//         <div class="col-1">
//             <div class="btn-group">
//                 <button class="btn btn-warning border-0" title="Modify Ingredient" name="modify">
//                     <i class="bi bi-pencil-square"></i>
//                 </button>
//                 <button class="btn btn-danger border-0" title="Remove Ingredient" name="remove">
//                     <i class="bi bi-trash3-fill"></i>
//                 </button>
//             </div>
//         </div>
//     </div>`
// );

// table.find("[name='modify']").on("click", modify);
// table.find("[name='remove']").on("click", remove);