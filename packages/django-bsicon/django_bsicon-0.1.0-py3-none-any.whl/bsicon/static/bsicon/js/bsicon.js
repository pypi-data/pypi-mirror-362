// bsicon/static/bsicon/js/bsicon.js
document.addEventListener('DOMContentLoaded', function() {
    // Selector widget integration
    document.querySelectorAll('.bsicon-selector-button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const fieldId = this.dataset.fieldId;
            const url = this.getAttribute('href');
            const win = window.open(
                url, 
                'bsicon_selector',
                'width=800,height=600,resizable=yes,scrollbars=yes'
            );
            win.name = fieldId;
        });
    });
    
    // Icon selector functionality (for the popup)
    if (document.getElementById('bsicon-container')) {
        const iconList = new List('bsicon-container', {
            valueNames: ['icon-name', 'data-styles'],
            searchClass: 'search',
            listClass: 'list'
        });
        
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const filter = this.dataset.filter;
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                if (filter === 'all') {
                    iconList.filter();
                } else {
                    iconList.filter(item => item.values().styles.includes(filter));
                }
            });
        });
        
        document.querySelectorAll('.icon-preview').forEach(icon => {
            icon.addEventListener('click', function() {
                const iconName = this.dataset.icon;
                window.opener.document.getElementById(window.name).value = iconName;
                window.close();
            });
        });
    }
});
