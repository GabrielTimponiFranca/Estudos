using System.Linq;
using System.Web.Mvc;
using Mvc_AngularDB.Models;

namespace Mvc_AngularDB.Controllers
{
    public class DBController : Controller
    {
        // GET: DB
        public ActionResult Index()
        {
            return View();
        }

        public JsonResult GetProduto()
        {
            Produto _produto = null;

            //define uma instância do contexto
            using (CadastroEntities dc = new CadastroEntities())
            {
                _produto = dc.Produtos.OrderByDescending(p => p.Id).Take(1).FirstOrDefault();
            }

            return new JsonResult { Data = _produto, JsonRequestBehavior = JsonRequestBehavior.AllowGet };
        }
    }
}