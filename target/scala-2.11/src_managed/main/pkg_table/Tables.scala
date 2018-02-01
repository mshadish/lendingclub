package pkg_table
// AUTO-GENERATED Slick data model
/** Stand-alone Slick data model for immediate use */
object Tables extends {
  val profile = slick.driver.SQLiteDriver
} with Tables

/** Slick data model trait for extension, choice of backend or usage in the cake pattern. (Make sure to initialize this late.) */
trait Tables {
  val profile: slick.driver.JdbcProfile
  import profile.api._
  import slick.model.ForeignKeyAction
  // NOTE: GetResult mappers for plain SQL are only generated for tables where Slick knows how to map the types of all columns.
  import slick.jdbc.{GetResult => GR}

  /** DDL for all tables. Call .create to execute. */
  lazy val schema: profile.SchemaDescription = Notes.schema ++ NotesHist.schema ++ NotesPlots.schema ++ NotesStg.schema
  @deprecated("Use .schema instead of .ddl", "3.0")
  def ddl = schema

  /** Entity class storing rows of table Notes
   *  @param id Database column id SqlType(NUM), PrimaryKey
   *  @param status Database column status SqlType(TEXT)
   *  @param statusDate Database column status_date SqlType(DATE)
   *  @param crawlDate Database column crawl_date SqlType(DATE)
   *  @param issueDate Database column issue_date SqlType(DATE) */
  case class NotesRow(id: Option[Double], status: Option[String], statusDate: Option[java.sql.Date], crawlDate: Option[java.sql.Date], issueDate: Option[java.sql.Date])
  /** GetResult implicit for fetching NotesRow objects using plain SQL queries */
  implicit def GetResultNotesRow(implicit e0: GR[Option[Double]], e1: GR[Option[String]], e2: GR[Option[java.sql.Date]]): GR[NotesRow] = GR{
    prs => import prs._
    NotesRow.tupled((<<?[Double], <<?[String], <<?[java.sql.Date], <<?[java.sql.Date], <<?[java.sql.Date]))
  }
  /** Table description of table notes. Objects of this class serve as prototypes for rows in queries. */
  class Notes(_tableTag: Tag) extends Table[NotesRow](_tableTag, "notes") {
    def * = (id, status, statusDate, crawlDate, issueDate) <> (NotesRow.tupled, NotesRow.unapply)

    /** Database column id SqlType(NUM), PrimaryKey */
    val id: Rep[Option[Double]] = column[Option[Double]]("id", O.PrimaryKey)
    /** Database column status SqlType(TEXT) */
    val status: Rep[Option[String]] = column[Option[String]]("status")
    /** Database column status_date SqlType(DATE) */
    val statusDate: Rep[Option[java.sql.Date]] = column[Option[java.sql.Date]]("status_date")
    /** Database column crawl_date SqlType(DATE) */
    val crawlDate: Rep[Option[java.sql.Date]] = column[Option[java.sql.Date]]("crawl_date")
    /** Database column issue_date SqlType(DATE) */
    val issueDate: Rep[Option[java.sql.Date]] = column[Option[java.sql.Date]]("issue_date")
  }
  /** Collection-like TableQuery object for table Notes */
  lazy val Notes = new TableQuery(tag => new Notes(tag))

  /** Entity class storing rows of table NotesHist
   *  @param id Database column id SqlType(NUM)
   *  @param status Database column status SqlType(TEXT)
   *  @param statusDate Database column status_date SqlType(DATE)
   *  @param crawlDate Database column crawl_date SqlType(DATE)
   *  @param issueDate Database column issue_date SqlType(DATE) */
  case class NotesHistRow(id: Option[Double], status: Option[String], statusDate: Option[java.sql.Date], crawlDate: Option[java.sql.Date], issueDate: Option[java.sql.Date])
  /** GetResult implicit for fetching NotesHistRow objects using plain SQL queries */
  implicit def GetResultNotesHistRow(implicit e0: GR[Option[Double]], e1: GR[Option[String]], e2: GR[Option[java.sql.Date]]): GR[NotesHistRow] = GR{
    prs => import prs._
    NotesHistRow.tupled((<<?[Double], <<?[String], <<?[java.sql.Date], <<?[java.sql.Date], <<?[java.sql.Date]))
  }
  /** Table description of table notes_hist. Objects of this class serve as prototypes for rows in queries. */
  class NotesHist(_tableTag: Tag) extends Table[NotesHistRow](_tableTag, "notes_hist") {
    def * = (id, status, statusDate, crawlDate, issueDate) <> (NotesHistRow.tupled, NotesHistRow.unapply)

    /** Database column id SqlType(NUM) */
    val id: Rep[Option[Double]] = column[Option[Double]]("id")
    /** Database column status SqlType(TEXT) */
    val status: Rep[Option[String]] = column[Option[String]]("status")
    /** Database column status_date SqlType(DATE) */
    val statusDate: Rep[Option[java.sql.Date]] = column[Option[java.sql.Date]]("status_date")
    /** Database column crawl_date SqlType(DATE) */
    val crawlDate: Rep[Option[java.sql.Date]] = column[Option[java.sql.Date]]("crawl_date")
    /** Database column issue_date SqlType(DATE) */
    val issueDate: Rep[Option[java.sql.Date]] = column[Option[java.sql.Date]]("issue_date")

    /** Primary key of NotesHist (database name pk_notes_hist) */
    val pk = primaryKey("pk_notes_hist", (id, statusDate))
  }
  /** Collection-like TableQuery object for table NotesHist */
  lazy val NotesHist = new TableQuery(tag => new NotesHist(tag))

  /** Entity class storing rows of table NotesPlots
   *  @param day Database column day SqlType(DATE), PrimaryKey
   *  @param defaultrate Database column defaultrate SqlType(REAL)
   *  @param defaultLateRate Database column default_late_rate SqlType(REAL)
   *  @param defaultLateGraceRate Database column default_late_grace_rate SqlType(REAL)
   *  @param totalNotes Database column total_notes SqlType(REAL) */
  case class NotesPlotsRow(day: Option[java.sql.Date], defaultrate: Option[Double], defaultLateRate: Option[Double], defaultLateGraceRate: Option[Double], totalNotes: Option[Double])
  /** GetResult implicit for fetching NotesPlotsRow objects using plain SQL queries */
  implicit def GetResultNotesPlotsRow(implicit e0: GR[Option[java.sql.Date]], e1: GR[Option[Double]]): GR[NotesPlotsRow] = GR{
    prs => import prs._
    NotesPlotsRow.tupled((<<?[java.sql.Date], <<?[Double], <<?[Double], <<?[Double], <<?[Double]))
  }
  /** Table description of table notes_plots. Objects of this class serve as prototypes for rows in queries. */
  class NotesPlots(_tableTag: Tag) extends Table[NotesPlotsRow](_tableTag, "notes_plots") {
    def * = (day, defaultrate, defaultLateRate, defaultLateGraceRate, totalNotes) <> (NotesPlotsRow.tupled, NotesPlotsRow.unapply)

    /** Database column day SqlType(DATE), PrimaryKey */
    val day: Rep[Option[java.sql.Date]] = column[Option[java.sql.Date]]("day", O.PrimaryKey)
    /** Database column defaultrate SqlType(REAL) */
    val defaultrate: Rep[Option[Double]] = column[Option[Double]]("defaultrate")
    /** Database column default_late_rate SqlType(REAL) */
    val defaultLateRate: Rep[Option[Double]] = column[Option[Double]]("default_late_rate")
    /** Database column default_late_grace_rate SqlType(REAL) */
    val defaultLateGraceRate: Rep[Option[Double]] = column[Option[Double]]("default_late_grace_rate")
    /** Database column total_notes SqlType(REAL) */
    val totalNotes: Rep[Option[Double]] = column[Option[Double]]("total_notes")
  }
  /** Collection-like TableQuery object for table NotesPlots */
  lazy val NotesPlots = new TableQuery(tag => new NotesPlots(tag))

  /** Entity class storing rows of table NotesStg
   *  @param id Database column id SqlType(NUM)
   *  @param status Database column status SqlType(TEXT)
   *  @param statusDate Database column status_date SqlType(DATE)
   *  @param crawlDate Database column crawl_date SqlType(DATE)
   *  @param issueDate Database column issue_date SqlType(DATE) */
  case class NotesStgRow(id: Option[Double], status: Option[String], statusDate: Option[java.sql.Date], crawlDate: Option[java.sql.Date], issueDate: Option[java.sql.Date])
  /** GetResult implicit for fetching NotesStgRow objects using plain SQL queries */
  implicit def GetResultNotesStgRow(implicit e0: GR[Option[Double]], e1: GR[Option[String]], e2: GR[Option[java.sql.Date]]): GR[NotesStgRow] = GR{
    prs => import prs._
    NotesStgRow.tupled((<<?[Double], <<?[String], <<?[java.sql.Date], <<?[java.sql.Date], <<?[java.sql.Date]))
  }
  /** Table description of table notes_stg. Objects of this class serve as prototypes for rows in queries. */
  class NotesStg(_tableTag: Tag) extends Table[NotesStgRow](_tableTag, "notes_stg") {
    def * = (id, status, statusDate, crawlDate, issueDate) <> (NotesStgRow.tupled, NotesStgRow.unapply)

    /** Database column id SqlType(NUM) */
    val id: Rep[Option[Double]] = column[Option[Double]]("id")
    /** Database column status SqlType(TEXT) */
    val status: Rep[Option[String]] = column[Option[String]]("status")
    /** Database column status_date SqlType(DATE) */
    val statusDate: Rep[Option[java.sql.Date]] = column[Option[java.sql.Date]]("status_date")
    /** Database column crawl_date SqlType(DATE) */
    val crawlDate: Rep[Option[java.sql.Date]] = column[Option[java.sql.Date]]("crawl_date")
    /** Database column issue_date SqlType(DATE) */
    val issueDate: Rep[Option[java.sql.Date]] = column[Option[java.sql.Date]]("issue_date")
  }
  /** Collection-like TableQuery object for table NotesStg */
  lazy val NotesStg = new TableQuery(tag => new NotesStg(tag))
}
