
fetch('files.json')
  .then(response => response.json())
  .then(files => {
    const createdFilesContainer = document.getElementById('created-files');
    const filePairsContainer = document.getElementById('file-pairs');
    
    
   const fileGroups = {};
    files.forEach(file => {
      const baseName = file.full_name.replace(/^original-|^replacing-|^created-/, '');
      fileGroups[baseName] = fileGroups[baseName] || {};
      fileGroups[baseName][file.type] = file;
    });
    
   for (const baseName in fileGroups) {
      const group = fileGroups[baseName];
      if (group['created'] && !group['original'] && !group['replacing']) {
                const createdFileBlock = document.createElement('div');
                createdFileBlock.classList.add('file-block');
                const fileNameDiv = document.createElement('div');
                fileNameDiv.classList.add('file-name');
                fileNameDiv.textContent = group['created'].full_name;
                const fileTypeDiv = document.createElement('div');
                fileTypeDiv.classList.add('file-type');
                fileTypeDiv.textContent = `Type: ${group['created'].type
}`;
                const codeBlockDiv = document.createElement('div');
                codeBlockDiv.classList.add('code-block');
                const codePre = document.createElement('pre');
                const codeCode = document.createElement('code');
                codeCode.classList.add('language-python');
                codeCode.textContent = group['created'].content;
                codePre.appendChild(codeCode);
                codeBlockDiv.appendChild(codePre);
                createdFileBlock.appendChild(fileNameDiv);
                createdFileBlock.appendChild(fileTypeDiv);
                createdFileBlock.appendChild(codeBlockDiv);
                createdFilesContainer.appendChild(createdFileBlock);
                Prism.highlightElement(codeCode);
            }
        }
        
       for (const baseName in fileGroups) {
            const group = fileGroups[baseName];
            const originalObj = group['original'];
            const replacingObj = group['replacing'];
      
            
           if (originalObj && replacingObj) {
              
             const fileBlock = document.createElement('div');
              fileBlock.classList.add('file-block');
      
              
             const fileNameDiv = document.createElement('div');
              fileNameDiv.classList.add('file-name');
              fileNameDiv.textContent = baseName; 
              fileBlock.appendChild(fileNameDiv);
      
              
             const diffHtml = generateLineByLineDiff(originalObj.content, replacingObj.content);
      
              
             const codeBlockDiv = document.createElement('div');
              codeBlockDiv.classList.add('code-block');
              codeBlockDiv.innerHTML = diffHtml;
              
              fileBlock.appendChild(codeBlockDiv);
              filePairsContainer.appendChild(fileBlock);
            }
            
            
           
         }
        });
      
      
     function generateLineByLineDiff(originalText, newText) {
        const diffResult = Diff.diffLines(originalText, newText);
        
       let html = '<pre>';
        diffResult.forEach(part => {
          const lines = escapeHtml(part.value).split('\n');
          lines.forEach(line => {
            if (part.added) {
              html += `<div class="diff-added">${line
}</div>`;
            } else if (part.removed) {
              html += `<div class="diff-removed">${line
}</div>`;
            } else {
                html += `<div class="diff-unchanged">${line
}</div>`;
            
            }
          });
        });
        html += '</pre>';
        return html;
      }
      
      
     function escapeHtml(str) {
        return str
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;');
      }
