/**
  * Created by mshadish on 8/20/16.
  */

object Tables extends {
  val profile = slick.driver.SQLiteDriver
} with pkg_table.Tables



import java.util.Calendar

import scalaj.http._
import scala.util.parsing.json._

import scala.concurrent.Await
import scala.concurrent.duration._
import scala.language.postfixOps


import Tables._
import Tables.profile.api._
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration.Duration

//import slick.driver.H2Driver.api._


import scala.concurrent.{Await, Future}
import scala.util.{Success, Failure}

object Sqlite extends App {
  val uri = sys.env.get("LENDINGCLUB_DB").get
  val db = Database.forURL(uri, driver="org.sqlite.JDBC")

  // get today's date
  val today = new java.sql.Date(Calendar.getInstance.getTime.getTime)

  def dateConvert(inval: String): java.sql.Date = {
    val dateParser = new java.text.SimpleDateFormat("yyyy-MM-dd")
    val java_type_date = dateParser.parse(inval)
    new java.sql.Date(java_type_date.getTime)
  }

  val f: Future[HttpResponse[String]] = Future {
    // will run get (instead of getOrElse) to throw compile-time error if var isn't properly defined
    val lendingclub_user: String = sys.env.get("LENDINGCLUB_USER").get
    val lendingclub = Http("https://api.lendingclub.com/api/investor/v1/accounts/" + lendingclub_user + "/notes")

    // get the authorization
    // will run get (instead of getOrElse) to throw compile-time error if var isn't properly defined
    val lendingclub_auth: String = sys.env.get("LENDINGCLUB_AUTH").get
    lendingclub.header("Content-Type", "application/json").header("Authorization", lendingclub_auth).asString
  }



  //f onComplete {
  val f2: Future[Unit] = f.map { lend_response => {
    //case Success(lend_response) => {
    val parsed_level1 = JSON.parseFull(lend_response.body) getOrElse ""
    val parsed_level2 = parsed_level1.asInstanceOf[Map[String, Any]] get "myNotes" getOrElse ""

    val all_notes = parsed_level2.asInstanceOf[List[Map[String, Any]]]
    val lendingclub_notes: List[(Option[Double], Option[String], Option[java.sql.Date], Option[java.sql.Date])] = all_notes map (x => ((x get "loanId").asInstanceOf[Option[Double]],
      (x get "loanStatus").asInstanceOf[Option[String]],
      Option(dateConvert((x get "loanStatusDate" get).asInstanceOf[String])),
      Option(dateConvert((x get "orderDate" get).asInstanceOf[String])))
      )
    val notes_to_insert = (lendingclub_notes map (a => NotesStgRow(a._1, a._2, a._3, Option(today), a._4))).toSeq
    Await.result(db.run(NotesStg ++= notes_to_insert), Duration.Inf)
    Await.result(db.run(sqlu"""
    insert or replace into notes (id, status, status_date, crawl_date, issue_date)
    select id, status, status_date, crawl_date, issue_date from notes_stg
    """), Duration.Inf)
    Await.result(db.run(sqlu"""
    insert or replace into notes_hist (id, status, status_date, crawl_date, issue_date)
    select id, status, status_date, crawl_date, issue_date from notes_stg
    """), Duration.Inf)
    Await.result(db.run(sqlu"delete from notes_stg"), Duration.Inf)
    //}
  }
  }
    //case Failure(exception) => throw new Error("unable")
  //}
  Await.result(f2, Duration.Inf)


  //db.run(sql"select count(1) from notes_stg".as[Int])
}