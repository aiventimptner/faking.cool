document.addEventListener('DOMContentLoaded', () => {
    const luxon = window.luxon;
    const format = 'dd.MM.yyyy HH:mm';

    (document.querySelectorAll('.choose-value').forEach(($button) => {
        let $input = $button.parentElement.parentElement.querySelector('input');

        if ($input.value) {
            let diff = luxon.DateTime.fromFormat($input.value, format) - luxon.DateTime.local();
            let value = Math.round(diff / 3600000);

            if (parseInt($button.value) === value) {
                $button.classList.add("is-active");
            }
        }

        $button.addEventListener('click', () => {
            let $buttons = $button.parentElement.querySelectorAll('button');
            $buttons.forEach(($button) => {
                $button.classList.remove("is-active");
            });

            $button.classList.add("is-active");

            let now = luxon.DateTime.local();
            $input.value = now.plus({hours: $button.value}).toFormat(format);
        });
    }));
});