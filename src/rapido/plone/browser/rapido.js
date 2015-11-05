require([
    'jquery',
    'mockup-patterns-base',
    'pat-registry'
], function($, Base, Registry) {
    'use strict';
    var Rapido = Base.extend({
        name: 'rapido',
        trigger: '.rapido-block',
        defaults: {},
        init: function() {
            var self = this;
            self.settings = JSON.parse(self.$el.attr('rapido-settings'));
            if(self.$el.hasClass('rapido-target-ajax')) {
                self.initAjaxForm();
            }
            if(self.settings.debug) {
                self.showDebug();
            }
        },
        initAjaxForm: function() {
            var self = this;
            var ajax_submit = function(event){
                var formData = self.$el.serializeArray();
                if(this.prop("tagName")=='INPUT') {
                    formData.push({
                        name: this.attr('name'),
                        value: this.val()
                    });
                }
                $.ajax({
                    url: self.$el.attr('action'),
                    type: self.$el.attr('method'),
                    dataType:'html',
                    data: formData,
                    success: function(response, textStatus, jqXHR){
                        var $content = $(response);
                        self.$el.replaceWith($content);
                        Registry.scan($content);
                        self.initAjaxForm();
                    },
                    error: function(jqXHR, textStatus, errorThrown){
                        console.log('error(s):'+textStatus, errorThrown);
                    }
                });
                return false;
            };
            self.$el.submit(ajax_submit.bind(self.$el));
            self.$el.find('input[type=submit]').each(function(i, el) {
                $(el).click(ajax_submit.bind($(el)));
            });
        },
        showDebug: function() {
            var self = this;
            $.getJSON(self.settings.url + '/_log', function(data) {
                $.each(data, function(i, item) {
                    console.log(item);
                });
            })
        }
    });
    return Rapido;
});