        $(document).on('click','.addClass',function(){
            $('.block:last').before('<div class="input-group mb-3 testing" id="newClassRow"><input type="text" id="newClass" class="form-control" placeholder="Class" aria-label="Recipient\'s username with two button addons"><button type="button" onclick="" class="btn btn-danger delete">x</button></div>');
                      console.log(cumGPA.value);
        });

        $(document).on('click', '.delete',function(){
        $(this).parent().remove();
        });

        $(document).on('click', '.clear',function(){
            $('#extraClassesHere').remove();
            $('.testing').before('<div id="extraClassesHere"><div id="newClassHere" class="block"></div></div>');
        });

        $("#cumQP").bind("input", function() {
        var cumGPA = parseInt($("#cumGPA").val()) || 0;
        var cumQP = parseInt($("#cumQP").val()) || 0;
        var gpa = (cumQP / cumGPA).toFixed(3);
        console.log(gpa);
        document.getElementById('currentGPA').innerHTML = gpa;
        });