name := "lendingclub"

version := "1.0"

scalaVersion := "2.11.8"


libraryDependencies +=  "org.scalaj" %% "scalaj-http" % "2.3.0"
libraryDependencies += "org.scala-lang.modules" %% "scala-parser-combinators" % "1.0.2"


libraryDependencies += "com.typesafe.slick" %% "slick" % "3.1.1"
libraryDependencies += "org.slf4j" % "slf4j-nop" % "1.6.4"
libraryDependencies += "com.typesafe.slick" %% "slick-codegen" % "3.1.1"
libraryDependencies += "org.xerial" % "sqlite-jdbc" % "3.8.10.1"



// causing server error
//libraryDependencies += "org.joda" % "joda-convert" % "1.8"



slick <<= slickCodeGenTask

sourceGenerators in Compile <+= slickCodeGenTask

lazy val slick = TaskKey[Seq[File]]("gen-tables")
lazy val slickCodeGenTask = (sourceManaged, dependencyClasspath in Compile, runner in Compile, streams) map { (dir, cp, r, s) =>
  val outputDir = (dir / "main").getPath

  val uri = sys.env.get("LENDINGCLUB_DB").get
  val jdbcDriver = "org.sqlite.JDBC"
  val slickDriver = "slick.driver.SQLiteDriver"
  val pkg = "pkg_table"
  toError(r.run("slick.codegen.SourceCodeGenerator", cp.files, Array(slickDriver, jdbcDriver, uri, outputDir, pkg), s.log))
  val fname = outputDir + "/" + pkg + "/Tables.scala"
  Seq(file(fname))
}
