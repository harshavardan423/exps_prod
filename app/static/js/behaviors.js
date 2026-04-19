(function () {
    var username = ATOM_USERNAME;

    document.querySelectorAll('.beh-toggle').forEach(function (toggle) {
        toggle.addEventListener('change', function (e) {
            e.stopPropagation();
            var behName = this.dataset.behavior;
            var isActive = this.checked;
            var url = isActive ? '/activate_behavior' : '/deactivate_behavior';
            fetch('/' + username + url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: behName })
            })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (!data.success) {
                    alert(data.error || 'Failed to ' + (isActive ? 'activate' : 'deactivate') + ' behavior');
                    toggle.checked = !isActive;
                }
            })
            .catch(function (err) {
                alert('Error: ' + err.message);
                toggle.checked = !isActive;
            });
        });
    });

    document.querySelectorAll('.seq-run').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            var seqName = this.dataset.sequence;
            var originalHtml = this.innerHTML;
            this.disabled = true;
            this.classList.add('playing');
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            fetch('/' + username + '/run_sequence', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: seqName })
            })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (data.error) throw new Error(data.error);
                btn.classList.remove('playing');
                btn.classList.add('done');
                btn.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(function () {
                    btn.classList.remove('done');
                    btn.innerHTML = originalHtml;
                    btn.disabled = false;
                }, 1500);
            })
            .catch(function (err) {
                btn.classList.remove('playing');
                btn.innerHTML = '<i class="fas fa-times"></i>';
                alert('Error: ' + err.message);
                setTimeout(function () {
                    btn.innerHTML = originalHtml;
                    btn.disabled = false;
                }, 1500);
            });
        });
    });
})();