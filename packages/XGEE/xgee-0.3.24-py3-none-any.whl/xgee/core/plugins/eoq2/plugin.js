//jsApplication plugin information

export async function init(pluginAPI,config) {  
    //plug-in statics and configuration
    let scriptIncludes=[
		"util/logger.js",
		"query/query.js",
		"command/command.js",
		"command/result.js",
		"frame/frame.js",
		"event/event.js",
		"domain/domain.js",
		"serialization/serializer.js",
		"serialization/jsonserializer.js",
		"serialization/textserializer.js",
		"domain/remote/websocketdomain.js",
        "legacy/legacy.js",
		"action/call.js",
		"eoq2.js",
    ];

    let stylesheetIncludes=[
    ];
    
	try {
		await pluginAPI.loadScripts(scriptIncludes);
		await pluginAPI.loadStylesheets(stylesheetIncludes);

		let instancePromises = [];
		for(let i=0;i<config.instances.length;i++) {
			let params = config.instances[i];
			
			let url = params.url;
			let logger = new eoq2.util.NoLogging();
			if($DEBUG) logger = new eoq2.util.ConsoleLogger(eoq2.util.DEFAULT_LOG_LEVELS.concat([eoq2.util.LogLevels.DEBUG]));
			let domain = new eoq2.domain.remote.WebSocketDomain(url,0,logger);
			instancePromises.push(domain.Open());
		}

		let domains = await Promise.all(instancePromises);

		let instances = {};
		let initSessionPromises = [];
		for(let i=0;i<config.instances.length;i++) {
			let params = config.instances[i];
			let user = params.user;
			let password = params.password;
			let domain = domains[i]; //domains must have the same length as config instances
			if(user && password) {
				initSessionPromises.push(domain.InitSession(user,password));
			}
			instances[params.eoq2DomainId] = domain;
			if(params.enableLegacy) {
				let legacyDomain = new eoq2.legacy.Jseoq1LegacyDomain(domain);
				instances[params.eoq1DomainId] = legacyDomain;
			}
		}
		await Promise.all(initSessionPromises);

		//register domain instances via the plugin api
		pluginAPI.expose({
			instances : instances
		});

		return true;

	}  catch (e) {
		throw e;
	}

};

export var meta={
    id : "eoq2",
    description : "JS implentation of Essential Object Query (EOQ) v2",
    author : "Bjoern Annighoefer",
	version  :"1.0.0",
	config : { 
		instances: [
			// {
			// 	eoq2DomainId: 'eoq2domain',
			// 	server : 'ws://localhost:8000/ws/eoq.do',
			//  user : 'admin',
			//  password : '!ToBeReplacedByTheRealPW_01!',
			// 	enableLegacy : true,
			// 	eoq1DomainId : 'legacyDomain'
			// }
		]
	  },
    requires:["eoq1"]
};




