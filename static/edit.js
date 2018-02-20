

$("#pdfexport").click(function(){
  var html= $("#x").val();
  var doc= new jsPDF();
  doc.fromHTML(html,20,20,{'width':1000});
  doc.save('Test.pdf');


});
