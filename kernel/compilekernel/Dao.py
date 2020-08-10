import pymysql

class Dao:

    #执行方法
    def executeSql(self,sql):
        conn = pymysql.connect("localhost","root","123456","klinux")
        try:
            cur=conn.cursor()
            cur.execute(sql)
            conn.commit()
        except Exception:
            print(Exception)
            print("执行错误，回滚")
            conn.rollback()
        finally:
            conn.close()
            cur.close()

    #查询方法
    def executeQuerySql(self,sql):
        conn = pymysql.connect("localhost","root","123456","klinux")
        try:
            cur=conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            return res
        except Exception:
            print(Exception)
            print("执行错误，回滚")
            conn.rollback()
        finally:
            conn.close()
            cur.close()

dao = Dao()
username = 'zhubin'
uid=1
results =  dao.executeQuerySql("select * from tbl_record where id = (select max(id) from tbl_record) and uid = '%s' " % (uid))[0]
print(results)
