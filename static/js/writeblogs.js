$(document).ready(function(){
     $("#My").click();
});

$("#All").on('click', function(e){
        $('#container').html('');
        e.preventDefault();
        var title,taglist,content,date,tags,htmlcont,i,k;
        htmlcont = '</br></br></br><div id= "container">';
        $.getJSON('/allblogs', function(data){

            for(i=0; i<Object.keys(data).length; i++){
            title = data[i].title;
            taglist = data[i].tags;
            content = data[i].content;
            date = data[i].date;
            id = data[i].id;
            username = data[i].username;

            tags = taglist.split(',');

            htmlcont += '<div id = "blogs">';
            htmlcont += '<p id = "blogsname">'+ username +'</p>'
            htmlcont += '<h2 id = "blogsheading">' + title + '</h2><hr/ width="60%" align="left">';
            htmlcont += '<p id = "blogsdate">' + date + '</p>'
            htmlcont += '<table id = "blogstable"><tr>'
            for(k=0; k < tags.length; k++){
            htmlcont += '<td id= "blogstags">'+ tags[k] + '</td>'
            }
            htmlcont += '</tr></table><p id="blogscontent">'+ content +'</p></div></br>'
            if (i == Object.keys(data).length){
            htmlcont += '</div>'
            }
            /* $('#userpagemenu').after('<br/><br/><br/><div id= "container"><div id = "blogs"><button id = "blogdelete"> Delete </button><button id = "blogsshare"> Share </button><h2 id = "blogsheading"> Title </h2><hr/ width="60%" align="left"><p id = "blogsdate"> 20, January, 2020 </p><table id = "blogstable"><tr><td id= "blogstags"> Inspirational </td><td id= "blogstags"> Educational </td><td id= "blogstags"> Scientific </td><td id= "blogstags"> Comic </td><td id= "blogstags"> Religious </td></tr></table><p id="blogscontent"> This is just a sample blog thank you for such a wonderful blogpostI think I can do whatever I can to make this blog .'); */

            }
            $('#userpagemenu').after(htmlcont);

        });
        });

$("#My").on('click', function(e){
        $('#container').html('');
        e.preventDefault();
        var title,taglist,content,date,tags,htmlcont,i,k;
        htmlcont = '</br></br></br><div id= "container">'
        $.getJSON('/myblogs', function(data){
            if (data[0] == null){
            var intro;
            intro ='</br></br></br><div id = "container"><div id = "blogsintro"><p id = "blogintroheading"> Start your first blog.....</p></div></div>'
            $("#container").html('');
            $("#userpagemenu").after(intro);
            }
            else{
            for(i=0; i<Object.keys(data).length; i++){
            title = data[i].title;
            taglist = data[i].tags;
            content = data[i].content;
            date = data[i].date;
            id = data[i].id;

            tags = taglist.split(',');

            htmlcont += '<div id = "blogs"><button id = "blogdelete" class = "blogdeletebutton" name = "delete" value= '+ id +'> Delete </button><button id = "blogsshare" class = "blogsharebutton" name = "share" value = ' + id + '> Share </button>';

            htmlcont += '<h2 id = "blogsheading">' + title + '</h2><hr/ width="60%" align="left">';
            htmlcont += '<p id = "blogsdate">' + date + '</p>';
            htmlcont += '<table id = "blogstable"><tr>'
            for(k=0; k < tags.length; k++){
            htmlcont += '<td id= "blogstags">'+ tags[k] + '</td>'
            }
            htmlcont += '</tr></table><p id="blogscontent">'+ content +'</p></div></br></br></br>'
            if (i == Object.keys(data).length){
            htmlcont += '</div>'
            }
            /* $('#userpagemenu').after('<br/><br/><br/><div id= "container"><div id = "blogs"><button id = "blogdelete"> Delete </button><button id = "blogsshare"> Share </button><h2 id = "blogsheading"> Title </h2><hr/ width="60%" align="left"><p id = "blogsdate"> 20, January, 2020 </p><table id = "blogstable"><tr><td id= "blogstags"> Inspirational </td><td id= "blogstags"> Educational </td><td id= "blogstags"> Scientific </td><td id= "blogstags"> Comic </td><td id= "blogstags"> Religious </td></tr></table><p id="blogscontent"> This is just a sample blog thank you for such a wonderful blogpostI think I can do whatever I can to make this blog .'); */

            }
            $('#userpagemenu').after(htmlcont);
            $("button.blogsharebutton").on('click', function(){

               var jsid = {'id': $(this).val()};


               $.ajax({
                    type: "POST",
                    url: "/shareblog",
                    data: JSON.stringify(jsid),
                    contentType: "application/json",
               }).done(

               )
               $(this).html('Shared');

        });
            $("button.blogdeletebutton").on('click', function(){

               var jsid = {'id': $(this).val()};


               $.ajax({
                    type: "POST",
                    url: "/deleteblog",
                    data: JSON.stringify(jsid),
                    contentType: "application/json",
               }).done(

               )

               $("#My").click();

        });
        }
        });
        });


$('#Shared').on('click', function(e){
        $('#container').html('');
        e.preventDefault();
        var title,taglist,content,date,tags,htmlcont,i,k;
        htmlcont = '</br></br></br><div id= "container">'
        $.getJSON('/sharedblogs', function(data){
            for(i=0; i<Object.keys(data).length; i++){
            title = data[i].title;
            taglist = data[i].tags;
            content = data[i].content;
            date = data[i].date;
            id = data[i].id;

            tags = taglist.split(',');

            htmlcont += '<div id = "blogs">';

            htmlcont += '<h2 id = "blogsheading">' + title + '</h2><hr/ width="60%" align="left">';
            htmlcont += '<p id = "blogsdate">' + date + '</p>'
            htmlcont += '<table id = "blogstable"><tr>'
            for(k=0; k < tags.length; k++){
            htmlcont += '<td id= "blogstags">'+ tags[k] + '</td>'
            }
            htmlcont += '</tr></table><p id="blogscontent">'+ content +'</p></div></br></br></br>'
            if (i == Object.keys(data).length){
            htmlcont += '</div>'
            }
            /* $('#userpagemenu').after('<br/><br/><br/><div id= "container"><div id = "blogs"><button id = "blogdelete"> Delete </button><button id = "blogsshare"> Share </button><h2 id = "blogsheading"> Title </h2><hr/ width="60%" align="left"><p id = "blogsdate"> 20, January, 2020 </p><table id = "blogstable"><tr><td id= "blogstags"> Inspirational </td><td id= "blogstags"> Educational </td><td id= "blogstags"> Scientific </td><td id= "blogstags"> Comic </td><td id= "blogstags"> Religious </td></tr></table><p id="blogscontent"> This is just a sample blog thank you for such a wonderful blogpostI think I can do whatever I can to make this blog .'); */

            }
            $('#userpagemenu').after(htmlcont);
        });
        });


$("#New").on('click', function(e){
        e.preventDefault();
        $('#container').html('');
        $("#userpagemenu").after('<br/><br/><br/><div id= "container"><form id="blogsform" action= "/blogdata" method= "POST"><input type= "hidden"  value = {{ username }} name = "username" /><label id= "blogsformtitle"> Title on your mind? <br/><br/><input id = "blogsformtitleinput" type= "text" name= "blogstitleinput"/></label><br/><br/><p id= "blogsformtagspara">Select the tags for blogs:</p><input value="education" name="blogstag" type="checkbox"/>Educational<input value="inspiration" name="blogstag" type="checkbox"/>Inspirational<input value="scientific" name="blogstag" type="checkbox"/>Scientific<input value="comic" name="blogstag" type="checkbox"/>Comic<input value="religious" name="blogstag" type="checkbox"/>Religious<input value="factual" name="blogstag" type="checkbox"/>Factual<input value="news" name="blogstag" type="checkbox"/>News<input value="family" name="blogstag" type="checkbox"/>Family<input value="any" name="blogstag" type="checkbox"/>Any<br/><br/><label id= "blogsformcontent">Write your blog: <br/><br/><textarea id= "blogsformcontentinput" name= "blogscontentinput">Make it short and cool...</textarea></label><br/><br/><input type="submit" name="submit" id="submit"/></form></div>');
        $("#blogsform").on('submit', function(e){
        e.preventDefault();
        var details = $("#blogsform").serialize();
        $.post('/blogdata', details, function(){
                $('#container').html('');
                $('#All').click();
        });
        });
        });

$('#Search').on('click', function(e){
        var resultjson;
        e.preventDefault();
        $('#container').html('');
        $('#userpagemenu').after('</br></br></br><div id = "container"><div id = "blogssearch"><p id = "blogsearchheading"> BunnyBlog Search</p><input type="text" name="blogssearch" id = "blogssearchinput" value="Search by blog tags"/><button id = "searchbutton">Search</button><div id= "blogssearchcontainer"></div></div></div>');

         $("input").keyup(function(){
            jsresults = {'suggestion': $("input").val()};
            $.ajax({
            url: "/searchblog",
            type: "POST",
            data: JSON.stringify(jsresults),

            success: function(data){
            resultjson = JSON.parse(data);
            var result = resultjson['result'].split(',');
            var introcont = '<p id = "resultsintro"> Search results: </p>'
            var htmlcont = '';
            var i;
            for(i=0; i<result.length; i++){
                htmlcont += '<p id = "results">'+ result[i] +'</p>'
            }
            $('#blogssearchcontainer').html(introcont+htmlcont)
            },

            contentType: "application/json"
            })
            });

/* Search button starts here */

            $("#searchbutton").on('click', function(e){
                $.ajax({
                url: "/searchresult",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(resultjson),
                success: function(data){
                    var title,taglist,content,date,tags,htmlcont,i,k;
                    var data = JSON.parse(data);
                    htmlcont = '<div id = "container">'
                    for(i=0; i<Object.keys(data).length; i++){
                    title = data[i].title;
                    taglist = data[i].tags;
                    content = data[i].content;
                    date = data[i].date;
                    id = data[i].id;
                    tags = taglist.split(',');

                    htmlcont += '<div id = "blogs">';

                    htmlcont += '<h2 id = "blogsheading">' + title + '</h2><hr/ width="60%" align="left">';
                    htmlcont += '<p id = "blogsdate">' + date + '</p>'
                    htmlcont += '<table id = "blogstable"><tr>'
                    for(k=0; k < tags.length; k++){
                    htmlcont += '<td id= "blogstags">'+ tags[k] + '</td>'
                    }
                    htmlcont += '</tr></table><p id="blogscontent">'+ content +'</p></div></br></br></br>'
                    if (i == Object.keys(data).length){
                    htmlcont += '</div>'
                    }
                    /* $('#userpagemenu').after('<br/><br/><br/><div id= "container"><div id = "blogs"><button id = "blogdelete"> Delete </button><button id = "blogsshare"> Share </button><h2 id = "blogsheading"> Title </h2><hr/ width="60%" align="left"><p id = "blogsdate"> 20, January, 2020 </p><table id = "blogstable"><tr><td id= "blogstags"> Inspirational </td><td id= "blogstags"> Educational </td><td id= "blogstags"> Scientific </td><td id= "blogstags"> Comic </td><td id= "blogstags"> Religious </td></tr></table><p id="blogscontent"> This is just a sample blog thank you for such a wonderful blogpostI think I can do whatever I can to make this blog .'); */

                    }
                    $('#container').html('');
                    $('#userpagemenu').after(htmlcont);
                        }
                        });
            });

/* Search button ends here */

        });




