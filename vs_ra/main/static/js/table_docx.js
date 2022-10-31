
document.getElementById('download').onclick = () => {
    const base64 = '{{ docx }}'
    const link = document.createElement('a');
    link.href = 'data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,' + base64;
    link.download = 'my-document.docx';
    link.click();
};