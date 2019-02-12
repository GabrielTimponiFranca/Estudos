using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(Mvc_AngularDB.Startup))]
namespace Mvc_AngularDB
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
