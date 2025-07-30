$(document).ready(function () {
    $('select').each(function () {
        const select = $(this);
        const es_multiple = select.is('[multiple]');
        
        let config = {
            width: '100%'
        };

        if (es_multiple) config.placeholder = select.attr('placeholder');

        if (!es_multiple && select.children().not('[value=""]').length <= 3) config.minimumResultsForSearch = Infinity;

        select.select2(config);
    });
});
