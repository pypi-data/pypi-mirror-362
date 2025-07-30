function generate_production_request_guid() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }

    return s4() + s4() + s4();
}

function formatDate(d) {
    return (
        d.getFullYear() + '-' + d.getMonth() + '-' + d.getDate() + ' ' +
        d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds() + '.' +
        d.getMilliseconds())
}

// Общий UUID клиента для всех запросов
var clientUUID = generate_production_request_guid();
var productionRequestLogStore = [];
var productionRequestExcludeUrls = [];

XhrInterceptor.addRequestCallback(function(xhr) {
    try {
        xhr.setRequestHeader('PR-UUID', clientUUID + '#' + generate_production_request_guid());
        xhr.setRequestHeader('PR-C-STARTED', Date.now());
    } catch (e) {
        console.log("Can't set production request headers. Details:", e.error.toString());
    }
});

XhrInterceptor.addResponseCallback(function(xhr) {
    try {
        var req_uuid = xhr.getResponseHeader('PR-UUID');
        var req_started = xhr.getResponseHeader('PR-C-STARTED');
        if (req_uuid && req_started) {
            req_started = parseInt(req_started, 10);
            var addToLog = true;

            if (productionRequestExcludeUrls.length) {
                for (var i = 0; i < productionRequestExcludeUrls.length; i++) {
                    if (xhr.responseURL.indexOf(productionRequestExcludeUrls[i]) !== -1) {
                        addToLog = false;
                        break;
                    }
                }
            }

            var s_total = parseFloat(xhr.getResponseHeader('PR-TOTAL') || 0);
            var s_sql_total = parseFloat(xhr.getResponseHeader('PR-SQL-TOTAL') || 0);

            if (addToLog) {
                var record = {
                    'uuid': req_uuid,
                    'c_path': xhr.responseURL,
                    'c_total': Math.max(Date.now() - req_started, s_total, 0),
                    'started': xhr.getResponseHeader('PR-STARTED') || '',
                    'path': xhr.getResponseHeader('PR-PATH') || '',
                    'is_success': xhr.getResponseHeader('PR-IS-SUCCESS') || true,
                    'user': xhr.getResponseHeader('PR-USER') || '',
                    'hostname': xhr.getResponseHeader('PR-HOSTNAME') || '',
                    'total': s_total,
                    'sql_total': s_sql_total,
                    'sync_sql_total': parseFloat(xhr.getResponseHeader('PR-SYNC-SQL-TOTAL') || 0),
                    'async_sql_total': parseFloat(xhr.getResponseHeader('PR-ASYNC-SQL-TOTAL') || 0),
                    'sync_sql_s_total': parseFloat(xhr.getResponseHeader('PR-SQL-S-TOTAL') || xhr.getResponseHeader('PR-SYNC-SQL-S-TOTAL') || 0),
                    'sync_sql_i_total': parseFloat(xhr.getResponseHeader('PR-SQL-I-TOTAL') || xhr.getResponseHeader('PR-SYNC-SQL-I-TOTAL') || 0),
                    'sync_sql_u_total': parseFloat(xhr.getResponseHeader('PR-SQL-U-TOTAL') || xhr.getResponseHeader('PR-SYNC-SQL-U-TOTAL') || 0),
                    'sync_sql_d_total': parseFloat(xhr.getResponseHeader('PR-SQL-D-TOTAL') || xhr.getResponseHeader('PR-SYNC-SQL-D-TOTAL') || 0),
                    'sync_sql_c_total': parseFloat(xhr.getResponseHeader('PR-SQL-C-TOTAL') || xhr.getResponseHeader('PR-SYNC-SQL-C-TOTAL') || 0),
                    'sql_count': parseInt(xhr.getResponseHeader('PR-SQL-COUNT') || 0),
                    'sync_sql_count': parseInt(xhr.getResponseHeader('PR-SYNC-SQL-COUNT') || xhr.getResponseHeader('PR-SQL-COUNT') || 0),
                    'async_sql_count': parseInt(xhr.getResponseHeader('PR-ASYNC-SQL-COUNT') || 0),
                    'sync_sql_s_count': parseInt(xhr.getResponseHeader('PR-SQL-S-COUNT') || xhr.getResponseHeader('PR-SYNC-SQL-S-COUNT') || 0),
                    'async_sql_s_count': parseInt(xhr.getResponseHeader('PR-ASYNC-SQL-S-COUNT') || 0),
                    'sync_sql_i_count': parseInt(xhr.getResponseHeader('PR-SQL-I-COUNT') || xhr.getResponseHeader('PR-SYNC-SQL-I-COUNT') || 0),
                    'async_sql_i_count': parseInt(xhr.getResponseHeader('PR-ASYNC-SQL-I-COUNT') || 0),
                    'sync_sql_u_count': parseInt(xhr.getResponseHeader('PR-SQL-U-COUNT') || xhr.getResponseHeader('PR-SYNC-SQL-U-COUNT') || 0),
                    'async_sql_u_count': parseInt(xhr.getResponseHeader('PR-ASYNC-SQL-U-COUNT') || 0),
                    'sync_sql_d_count': parseInt(xhr.getResponseHeader('PR-SQL-D-COUNT') || xhr.getResponseHeader('PR-SYNC-SQL-D-COUNT') || 0),
                    'async_sql_d_count': parseInt(xhr.getResponseHeader('PR-ASYNC-SQL-D-COUNT') || 0),
                    'sync_sql_c_count': parseInt(xhr.getResponseHeader('PR-SQL-C-COUNT') || xhr.getResponseHeader('PR-SYNC-SQL-C-COUNT') || 0),
                    'async_sql_c_count': parseInt(xhr.getResponseHeader('PR-ASYNC-SQL-C-COUNT') || 0),
                    'sync_sql_sp_count': parseInt(xhr.getResponseHeader('PR-SQL-SP-COUNT') || xhr.getResponseHeader('PR-SYNC-SQL-SP-COUNT') || 0),
                    'async_sql_sp_count': parseInt(xhr.getResponseHeader('PR-ASYNC-SQL-SP-COUNT') || 0),
                    'sync_sql_j_count': parseInt(xhr.getResponseHeader('PR-SQL-J-COUNT') || xhr.getResponseHeader('PR-SYNC-SQL-J-COUNT') || 0),
                    'async_sql_j_count': parseInt(xhr.getResponseHeader('PR-ASYNC-SQL-J-COUNT') || 0),
                    'sync_sql_di_count': parseInt(xhr.getResponseHeader('PR-SQL-DI-COUNT') || xhr.getResponseHeader('PR-SYNC-SQL-DI-COUNT') || 0),
                    'async_sql_di_count': parseInt(xhr.getResponseHeader('PR-ASYNC-SQL-DI-COUNT') || 0),
                    'sync_sql_gb_count': parseInt(xhr.getResponseHeader('PR-SQL-GB-COUNT') || xhr.getResponseHeader('PR-SYNC-SQL-GB-COUNT') || 0),
                    'async_sql_gb_count': parseInt(xhr.getResponseHeader('PR-ASYNC-SQL-GB-COUNT') || 0),
                    'sql_duplicate_count': parseInt(xhr.getResponseHeader('PR-SQL-DUPLICATE-COUNT') || 0),
                    'sql_transaction_count': parseInt(xhr.getResponseHeader('PR-SQL-TRANSACTION-COUNT') || 0),
                    'sql_transaction_total': parseFloat(xhr.getResponseHeader('PR-SQL-TRANSACTION-TOTAL') || 0),
                    'sql_db_aliases': xhr.getResponseHeader('PR-SQL-DB-ALIASES') || '',
                    'app_total': (s_total - s_sql_total).toFixed(4),
                    'client_ip': xhr.getResponseHeader('PR-CLIENT-IP') || '',
                    'pid': xhr.getResponseHeader('PR-PID') || '',
                    'uss': parseFloat(xhr.getResponseHeader('PR-USS') || 0),
                    'pss': parseFloat(xhr.getResponseHeader('PR-PSS') || 0),
                    'swap': parseFloat(xhr.getResponseHeader('PR-SWAP') || 0),
                    'rss': parseFloat(xhr.getResponseHeader('PR-RSS') || 0),
                };
                var customHeadersStr = xhr.getResponseHeader('PR-CUSTOM');
                if (customHeadersStr) {
                    var customHeaders = customHeadersStr.split(',');
                    customHeaders.forEach(function(header) {
                        if (header) {
                            var key =  header.replace('PR-', '').split('-').join('_').toLowerCase();
                            record[key] = xhr.getResponseHeader(header);
                        }
                    });
                }
                record['tr_total'] = (record['c_total'] - record['total']).toFixed(4);
                productionRequestLogStore.push(record);
            }
        }
    } catch (e) {
        console.log("Can't process production response. Details:", e.error.toString());
    }
});
// Подключаемся к запросам
XhrInterceptor.wire();

function startLogging(clientLogUrl, timeout = 10000) {
    function sendProductionRequestStats() {
        if (productionRequestLogStore.length) {
            var log_part = productionRequestLogStore.slice();
            productionRequestLogStore = [];
            Ext.Ajax.request({
                url: clientLogUrl,
                method: 'POST',
                params: {
                    'logs': Ext.util.JSON.encode(log_part)
                },
                success: function (response) {
                },
                failure: function () {
                    productionRequestLogStore.concat(log_part)
                }
            });
        }
    }

    productionRequestExcludeUrls.push(clientLogUrl);
    setInterval(sendProductionRequestStats, timeout);
}