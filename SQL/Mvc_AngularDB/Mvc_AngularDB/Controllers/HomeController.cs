using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using Mvc_AngularDB.Models;

namespace Mvc_AngularDB.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            return View();
        }

        public ActionResult DadosProduto() 
        {
            return View();
        }

        public ActionResult About()
        {
            ViewBag.Message = "Macoratti .net";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";

            return View();
        }
    }
}