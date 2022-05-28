function formExit() {
    document.getElementById("newForm").remove();
}

function myFunction(id) {
    if (document.contains(document.getElementById("newForm"))) {
        document.getElementById("newForm").remove();
    }
    
    var d1 = document.getElementById(id);
    d1.insertAdjacentHTML('afterend',
        '<form id="newForm" class="form-insert py-2" method="post"> \
            <div class="d-flex justify-content-between"><h5>Reply:</h5><div><button type="button" class="btn btn-outline-secondary btn-sm" onclick="formExit()"">Close</button></div></div> \
            <select name="parent" class="d-none" id="id_parentt"> \
            <option value="' + id + '" selected="' + id + '"></option> \
            </select> \
            <label for="id_content">Content:</label> \
            <textarea name="content" cols="40" rows="5" class="form-control" required id="id_content"></textarea> \
            {% csrf_token %} \
            <button type="submit" class="btn btn-success btn-block mt-2 btn-sm">Submit</button> \
        </form>');
        
}

// $('#myForm').trigger("reset");