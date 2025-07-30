#ifndef DBSPECIFIC_H
#define DBSPECIFIC_H

// Items specific to databases.
//
// Obviously we'd like to minimize this, but if they are needed this file isolates them.  I'd like for there to be a
// single build of pyodbc on each platform and not have a bunch of defines for supporting different databases.


// ---------------------------------------------------------------------------------------------------------------------
// SQL Server


#define SQL_SS_VARIANT -150     // SQL Server 2008 SQL_VARIANT type
#define SQL_SS_XML -152         // SQL Server 2005 XML type
#define SQL_DB2_DECFLOAT -360   // IBM DB/2 DECFLOAT type
#define SQL_DB2_XML -370        // IBM DB/2 XML type
#define SQL_SS_TIME2 -154       // SQL Server 2008 time type

struct SQL_SS_TIME2_STRUCT
{
   SQLUSMALLINT hour;
   SQLUSMALLINT minute;
   SQLUSMALLINT second;
   SQLUINTEGER  fraction;
};

// The SQLGUID type isn't always available when compiling, so we'll make our own with a
// different name.

struct PYSQLGUID
{
    // I was hoping to use uint32_t, etc., but they aren't included in a Python build.  I'm not
    // going to require that the compilers supply anything beyond that.  There is PY_UINT32_T,
    // but there is no 16-bit version.  We'll stick with Microsoft's WORD and DWORD which I
    // believe the ODBC headers will have to supply.
    DWORD Data1;
    WORD Data2;
    WORD Data3;
    byte Data4[8];
};

// this is "standard" but unix odbc doesn't always (ever?) have it
#ifndef SQL_BOOLEAN
#define	SQL_BOOLEAN	16
#endif

// LX-specific types
#ifndef SQL_LONGARRAY
#define	SQL_CIDR	(SQL_DRIVER_SQL_TYPE_BASE+1)
#define	SQL_LONGARRAY	(SQL_DRIVER_SQL_TYPE_BASE+2)
#define	SQL_DOUBLEARRAY	(SQL_DRIVER_SQL_TYPE_BASE+3)
#define	SQL_STRINGARRAY	(SQL_DRIVER_SQL_TYPE_BASE+4)
#define	SQL_OTHER	(SQL_DRIVER_SQL_TYPE_BASE+5)
#define	SQL_COLUMN_LIST	(SQL_DRIVER_SQL_TYPE_BASE+6)
#define	SQL_GEOMETRY	(SQL_DRIVER_SQL_TYPE_BASE+7)
#define	SQL_TIMESTAMP_LTZ	(SQL_DRIVER_SQL_TYPE_BASE+8)
#define	SQL_ARRAY	(SQL_DRIVER_SQL_TYPE_BASE+9)

// duplicated as usual for C
#define	SQL_C_CIDR	SQL_CIDR
#define	SQL_C_LONGARRAY	SQL_LONGARRAY
#define	SQL_C_DOUBLEARRAY	SQL_DOUBLEARRAY
#define	SQL_C_STRINGARRAY	SQL_STRINGARRAY
#define	SQL_C_OTHER	SQL_OTHER
#define	SQL_C_COLUMN_LIST	SQL_COLUMN_LIST
#define	SQL_C_GEOMETRY	SQL_GEOMETRY
#define	SQL_C_TIMESTAMP_LTZ	SQL_TIMESTAMP_LTZ
#define	SQL_C_ARRAY	SQL_ARRAY
#endif
#endif // DBSPECIFIC_H
