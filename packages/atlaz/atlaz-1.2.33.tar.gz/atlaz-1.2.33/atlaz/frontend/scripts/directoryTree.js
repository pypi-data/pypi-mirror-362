
fetch('http://127.0.0.1:5050/api/directory_tree')
    .then(response => response.json())
    .then(data => {
        const directoryData = data.tree; 
       const defaultUnmarked = data.default_unmarked; 
        const directoryTreeContainer = document.getElementById('directory-tree');
        const treeRoot = buildDirectoryTree(directoryData, defaultUnmarked);
        directoryTreeContainer.appendChild(treeRoot);
    })
    .catch(error => {
        console.error('Error fetching directory tree:', error);
    });
function buildDirectoryTree(data, defaultUnmarked) {
    const ul = document.createElement('ul');
    ul.classList.add('directory-list');
    data.forEach(item => {
        const li = createTreeItem(item, defaultUnmarked);
        ul.appendChild(li);
    });
    return ul;
}
function createTreeItem(item, defaultUnmarked) {
    const li = document.createElement('li');
    
   const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    
   
   checkbox.dataset.type = item.type;
    
   if (item.type === 'file') {
        checkbox.dataset.path = item.path; 
   } else {
        checkbox.dataset.path = ''; 
   }
    
   checkbox.id = `checkbox-${item.path.replace(/[^a-zA-Z0-9_\-]/g, '-')
}`;
    
   checkbox.checked = true;
    
   
   if (defaultUnmarked.some(u => item.path.includes(u))) {
        checkbox.checked = false;
    }
    
   const label = document.createElement('label');
    label.htmlFor = checkbox.id;
    label.textContent = item.name;
    
   li.appendChild(checkbox);
    li.appendChild(label);
    
   if (item.type === 'directory') {
        li.classList.add('directory');
        if (item.children && item.children.length > 0) {
            const childUl = document.createElement('ul');
            childUl.classList.add('nested-directory');
            item.children.forEach(childItem => {
                const childLi = createTreeItem(childItem, defaultUnmarked);
                childUl.appendChild(childLi);
            });
            li.appendChild(childUl);
            
           if (!checkbox.checked) {
                childUl.style.display = 'none'; 
            }
        }
    } else {
        
       li.classList.add('file');
    }
    
   checkbox.addEventListener('change', handleCheckboxChange);
    return li;
}
function handleCheckboxChange(event) {
    const checkbox = event.target;
    const li = checkbox.closest('li');
    const isChecked = checkbox.checked;
    
   if (li.classList.contains('directory')) {
        const childUl = li.querySelector('ul');
        if (childUl) {
            childUl.style.display = isChecked ? 'block' : 'none';
        }
        
       const childCheckboxes = li.querySelectorAll('ul li input[type="checkbox"]');
        childCheckboxes.forEach(childCb => {
            childCb.checked = isChecked;
            childCb.indeterminate = false;
        });
    }
    
   updateParentCheckboxes(li);
}
function updateParentCheckboxes(li) {
    const parentLi = li.parentElement.closest('li');
    if (!parentLi) return;
    const parentCheckbox = parentLi.querySelector('input[type="checkbox"]');
    if (!parentCheckbox) return;
    
   const siblingCheckboxes = parentLi.querySelectorAll('ul > li > input[type="checkbox"]');
    const allChecked = Array.from(siblingCheckboxes).every(cb => cb.checked);
    const someChecked = Array.from(siblingCheckboxes).some(cb => cb.checked || cb.indeterminate);
    if (allChecked) {
        parentCheckbox.checked = true;
        parentCheckbox.indeterminate = false;
    } else if (someChecked) {
        parentCheckbox.checked = false;
        parentCheckbox.indeterminate = true;
    } else {
        parentCheckbox.checked = false;
        parentCheckbox.indeterminate = false;
    }
    updateParentCheckboxes(parentLi);
}
function gatherSelectedPaths() {
    const checkedBoxes = document.querySelectorAll('input[type="checkbox"]:checked');
    const selectedPaths = [];
    checkedBoxes.forEach(cb => {
        
       if (cb.dataset.type === 'file' && cb.dataset.path) {
            selectedPaths.push(cb.dataset.path);
        }
    });
    return selectedPaths;
}
