document.addEventListener('DOMContentLoaded', () => {
    const luxon = window.luxon;

    (document.querySelectorAll('.set-value').forEach(($button) => {
        let $input = $button.parentElement.parentElement.querySelector('input');

        $button.addEventListener('click', () => {
            const format = 'dd.MM.yyyy HH:mm';

            let now;
            if ($input.value) {
                now = luxon.DateTime.fromFormat($input.value, format);
            } else {
                now = luxon.DateTime.local();
            }

            let dt;
            if (parseInt($button.value) === 0) {
                dt = luxon.DateTime.local();
            } else {
                dt = now.plus({minutes: $button.value});
            }

            $input.value = dt.toFormat(format);
        });
    }));
});