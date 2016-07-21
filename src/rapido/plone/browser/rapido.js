require([
    'jquery',
    'mockup-patterns-base',
    'pat-registry',
    'mockup-utils'
], function($, Base, Registry, utils) {
    'use strict';
    var Rapido = Base.extend({
        name: 'rapido',
        trigger: '.rapido-block',
        defaults: {},
        init: function() {
            var self = this;
            self.id = self.$el.attr('name');
            self.settings = JSON.parse(self.$el.attr('rapido-settings'));
            if(self.$el.hasClass('rapido-target-ajax')) {
                self.initAjaxForm();
            }
            self.ajaxLink();
            if(self.settings.app.debug) {
                self.showDebug();
            }
            self.loading = new utils.Loading();
            $(document).trigger('rapidoLoad', [self.id]);
        },
        initAjaxForm: function() {
            var self = this;
            var ajax_submit = function(event){
                var formData = self.$el.serializeArray();
                if(this.prop("tagName")=='INPUT' || this.prop("tagName")=='BUTTON') {
                    formData.push({
                        name: this.attr('name'),
                        value: this.val()
                    });
                }
                self.loading.show();
                $.ajax({
                    url: self.$el.attr('action'),
                    type: self.$el.attr('method'),
                    dataType:'html',
                    data: formData,
                    success: function(response, textStatus, jqXHR){
                        var $content = $(response);
                        self.$el.replaceWith($content);
                        Registry.scan($content);
                        self.loading.hide();
                    },
                    error: function(jqXHR, textStatus, errorThrown){
                        console.log('error(s):'+textStatus, errorThrown);
                        self.loading.hide();
                    }
                });
                return false;
            };
            self.$el.submit(ajax_submit.bind(self.$el));
            self.$el.find(':submit').each(function(i, el) {
                $(el).click(ajax_submit.bind($(el)));
            });
        },
        ajaxLink: function() {
            var self = this;
            var ajax_load = function(event){
                self.loading.show();
                $.ajax({
                    url: $(this).attr('href'),
                    type: 'GET',
                    dataType:'html',
                    success: function(response, textStatus, jqXHR){
                        var $content = $(response);
                        self.$el.replaceWith($content);
                        Registry.scan($content);
                        self.loading.hide();
                    },
                    error: function(jqXHR, textStatus, errorThrown){
                        console.log('error(s):'+textStatus, errorThrown);
                        self.loading.hide();
                    }
                });
                return false;
            };
            self.$el.find('a[target="ajax"]').each(function(i, el) {
                $(el).click(ajax_load.bind($(el)));
            });
        },
        showDebug: function() {
            var self = this;
            $.getJSON(self.settings.app.url + '/_log', function(data) {
                $.each(data, function(i, item) {
                    console.log(item);
                });
            })
        }
    });
    return Rapido;
});